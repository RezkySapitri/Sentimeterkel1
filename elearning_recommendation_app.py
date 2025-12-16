import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# ========================
# Konfigurasi Halaman
# ========================
st.set_page_config(
    page_title="Sistem Rekomendasi E-Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# CSS Styling
# ========================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stAlert {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# ========================
# Kelas Q-Learning Agent
# ========================
class QLearningAgent:
    """
    Agent Q-Learning untuk sistem rekomendasi e-learning
    """
    def __init__(self, n_states, n_actions, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = np.zeros((n_states, n_actions))
        self.training_history = []
        
    def get_action(self, state, training=True):
        """
        Memilih aksi menggunakan epsilon-greedy policy
        """
        if training and np.random.random() < self.epsilon:
            return np.random.randint(0, self.n_actions)  # Eksplorasi
        else:
            return np.argmax(self.q_table[state])  # Eksploitasi
    
    def update_q_value(self, state, action, reward, next_state):
        """
        Update Q-value menggunakan Q-Learning algorithm
        """
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state])
        new_q = current_q + self.lr * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state, action] = new_q
        
    def train(self, states, actions, rewards, next_states, episodes=100):
        """
        Melatih agent dengan data yang diberikan
        """
        n_samples = len(states)
        
        for episode in range(episodes):
            total_reward = 0
            indices = np.random.permutation(n_samples)
            
            for idx in indices:
                state = states[idx]
                action = actions[idx]
                reward = rewards[idx]
                next_state = next_states[idx]
                
                self.update_q_value(state, action, reward, next_state)
                total_reward += reward
            
            avg_reward = total_reward / n_samples
            self.training_history.append(avg_reward)
            
        return self.training_history

# ========================
# Fungsi Preprocessing Data
# ========================
@st.cache_data
def load_and_preprocess_data(file_path):
    """
    Memuat dan memproses data siswa
    """
    df = pd.read_csv(file_path)
    
    # Encoding kolom kategorikal
    le_gender = LabelEncoder()
    le_education = LabelEncoder()
    le_internet = LabelEncoder()
    le_lunch = LabelEncoder()
    le_activities = LabelEncoder()
    le_result = LabelEncoder()
    
    df['gender_encoded'] = le_gender.fit_transform(df['gender'])
    df['parent_education_encoded'] = le_education.fit_transform(df['parent_education'])
    df['internet_access_encoded'] = le_internet.fit_transform(df['internet_access'])
    df['lunch_type_encoded'] = le_lunch.fit_transform(df['lunch_type'])
    df['extra_activities_encoded'] = le_activities.fit_transform(df['extra_activities'])
    df['final_result_encoded'] = le_result.fit_transform(df['final_result'])
    
    # Hitung rata-rata skor
    df['avg_score'] = (df['math_score'] + df['reading_score'] + df['writing_score']) / 3
    
    # Kategorisasi performa (untuk state)
    df['performance_category'] = pd.cut(df['avg_score'], 
                                        bins=[0, 60, 75, 90, 100], 
                                        labels=['Low', 'Medium', 'High', 'Excellent'])
    
    # Kategorisasi jam belajar (untuk action)
    df['study_hours_category'] = pd.cut(df['study_hours'], 
                                        bins=[0, 2, 3.5, 5], 
                                        labels=['Low', 'Medium', 'High'])
    
    return df, le_gender, le_education, le_internet, le_lunch, le_activities, le_result

# ========================
# Fungsi Persiapan Data RL
# ========================
def prepare_rl_data(df):
    """
    Menyiapkan data untuk training Reinforcement Learning
    """
    # State: kombinasi performa dan karakteristik siswa
    state_features = ['performance_category', 'gender_encoded', 'grade_level', 
                     'internet_access_encoded', 'extra_activities_encoded']
    
    # Encode state
    df['state'] = df['performance_category'].astype('category').cat.codes
    
    # Action: jenis materi yang direkomendasikan (berdasarkan kategori jam belajar)
    df['action'] = df['study_hours_category'].astype('category').cat.codes
    
    # Reward: berdasarkan hasil akhir
    df['reward'] = df['final_result_encoded'] * 10 - 5  # Pass=5, Fail=-5
    
    # Next state (shifted)
    df['next_state'] = df['state'].shift(-1).fillna(df['state'].iloc[-1]).astype(int)
    
    return df

# ========================
# Fungsi Rekomendasi Materi
# ========================
def get_learning_material_recommendations(performance, action_type):
    """
    Memberikan rekomendasi materi pembelajaran berdasarkan performa dan tipe aksi
    """
    materials = {
        'Low': {
            0: ['Materi Dasar Matematika', 'Video Tutorial Interaktif', 'Quiz Dasar', 'Latihan Soal Level 1'],
            1: ['Materi Reading Comprehension', 'Flashcard Vocabulary', 'Bacaan Pendek', 'Audio Book'],
            2: ['Materi Writing Fundamental', 'Contoh Essay', 'Grammar Basic', 'Writing Practice']
        },
        'Medium': {
            0: ['Materi Matematika Menengah', 'Problem Solving', 'Quiz Level 2', 'Studi Kasus'],
            1: ['Reading Advanced', 'Critical Reading', 'Text Analysis', 'Literature Review'],
            2: ['Essay Writing', 'Academic Writing', 'Research Paper', 'Citation Methods']
        },
        'High': {
            0: ['Matematika Lanjut', 'Applied Mathematics', 'Research Topics', 'Competition Prep'],
            1: ['Advanced Reading', 'Research Papers', 'Academic Journals', 'Critical Essays'],
            2: ['Advanced Writing', 'Thesis Writing', 'Publication Guide', 'Academic Papers']
        },
        'Excellent': {
            0: ['Olimpiade Matematika', 'Higher Mathematics', 'Research Projects', 'Advanced Topics'],
            1: ['Expert Reading Materials', 'Scientific Journals', 'International Papers', 'Research Analysis'],
            2: ['Expert Writing', 'Publication Writing', 'Grant Proposals', 'Conference Papers']
        }
    }
    
    return materials.get(performance, {}).get(action_type, ['Materi Umum'])

# ========================
# Main Application
# ========================
def main():
    # Header
    st.markdown('<h1 class="main-header">📚 Sistem Rekomendasi E-Learning Berbasis Reinforcement Learning</h1>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/learning.png", width=100)
        st.title("⚙️ Pengaturan")
        
        uploaded_file = st.file_uploader("📂 Upload File CSV", type=['csv'])
        
        st.markdown("---")
        st.subheader("Parameter Q-Learning")
        learning_rate = st.slider("Learning Rate (α)", 0.01, 1.0, 0.1, 0.01)
        discount_factor = st.slider("Discount Factor (γ)", 0.0, 1.0, 0.9, 0.05)
        epsilon = st.slider("Epsilon (ε)", 0.0, 1.0, 0.1, 0.05)
        episodes = st.slider("Jumlah Episode", 50, 500, 100, 50)
        
        st.markdown("---")
        st.info("💡 **Tips**: Upload file student_info.csv untuk memulai analisis")
    
    # Main Content
    if uploaded_file is not None:
        try:
            # Load dan preprocess data
            with st.spinner('🔄 Memuat dan memproses data...'):
                df, le_gender, le_education, le_internet, le_lunch, le_activities, le_result = load_and_preprocess_data(uploaded_file)
            
            st.success(f"✅ Data berhasil dimuat! Total: {len(df)} siswa")
            
            # Tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📊 Eksplorasi Data", 
                "🤖 Training Model", 
                "🎯 Rekomendasi", 
                "📈 Analisis Hasil",
                "👤 Profil Siswa"
            ])
            
            # ==================== TAB 1: EKSPLORASI DATA ====================
            with tab1:
                st.markdown('<h2 class="sub-header">📊 Eksplorasi Data Siswa</h2>', unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Siswa", len(df))
                with col2:
                    pass_rate = (df['final_result'] == 'Pass').sum() / len(df) * 100
                    st.metric("Pass Rate", f"{pass_rate:.1f}%")
                with col3:
                    avg_score = df['avg_score'].mean()
                    st.metric("Rata-rata Skor", f"{avg_score:.1f}")
                with col4:
                    avg_study = df['study_hours'].mean()
                    st.metric("Rata-rata Jam Belajar", f"{avg_study:.1f} jam")
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Distribusi Gender
                    fig_gender = px.pie(df, names='gender', title='Distribusi Gender',
                                       color_discrete_sequence=px.colors.qualitative.Set3)
                    st.plotly_chart(fig_gender, use_container_width=True)
                    
                    # Distribusi Hasil
                    fig_result = px.histogram(df, x='final_result', color='final_result',
                                             title='Distribusi Hasil Belajar',
                                             color_discrete_sequence=['#ff6b6b', '#4ecdc4'])
                    st.plotly_chart(fig_result, use_container_width=True)
                
                with col2:
                    # Distribusi Skor
                    fig_scores = go.Figure()
                    fig_scores.add_trace(go.Box(y=df['math_score'], name='Math', marker_color='lightblue'))
                    fig_scores.add_trace(go.Box(y=df['reading_score'], name='Reading', marker_color='lightgreen'))
                    fig_scores.add_trace(go.Box(y=df['writing_score'], name='Writing', marker_color='lightcoral'))
                    fig_scores.update_layout(title='Distribusi Skor per Mata Pelajaran',
                                            yaxis_title='Skor')
                    st.plotly_chart(fig_scores, use_container_width=True)
                    
                    # Korelasi Study Hours vs Avg Score
                    fig_corr = px.scatter(df, x='study_hours', y='avg_score', 
                                         color='final_result',
                                         title='Korelasi Jam Belajar vs Rata-rata Skor',
                                         trendline="ols")
                    st.plotly_chart(fig_corr, use_container_width=True)
                
                # Performance Category
                st.markdown("### 📊 Kategori Performa Siswa")
                perf_dist = df['performance_category'].value_counts().reset_index()
                perf_dist.columns = ['Kategori', 'Jumlah']
                fig_perf = px.bar(perf_dist, x='Kategori', y='Jumlah', 
                                 color='Kategori',
                                 title='Distribusi Kategori Performa',
                                 color_discrete_sequence=px.colors.qualitative.Vivid)
                st.plotly_chart(fig_perf, use_container_width=True)
            
            # ==================== TAB 2: TRAINING MODEL ====================
            with tab2:
                st.markdown('<h2 class="sub-header">🤖 Training Model Q-Learning</h2>', unsafe_allow_html=True)
                
                if st.button("🚀 Mulai Training", type="primary", use_container_width=True):
                    with st.spinner('🔄 Melatih model Q-Learning...'):
                        # Prepare RL data
                        df_rl = prepare_rl_data(df.copy())
                        
                        # Get unique states and actions
                        n_states = df_rl['state'].nunique()
                        n_actions = df_rl['action'].nunique()
                        
                        st.info(f"📌 States: {n_states} | Actions: {n_actions}")
                        
                        # Initialize agent
                        agent = QLearningAgent(
                            n_states=n_states,
                            n_actions=n_actions,
                            learning_rate=learning_rate,
                            discount_factor=discount_factor,
                            epsilon=epsilon
                        )
                        
                        # Training
                        states = df_rl['state'].values
                        actions = df_rl['action'].values
                        rewards = df_rl['reward'].values
                        next_states = df_rl['next_state'].values
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        history = agent.train(states, actions, rewards, next_states, episodes=episodes)
                        
                        progress_bar.progress(100)
                        status_text.success("✅ Training selesai!")
                        
                        # Save agent to session state
                        st.session_state['agent'] = agent
                        st.session_state['df_rl'] = df_rl
                        st.session_state['n_states'] = n_states
                        st.session_state['n_actions'] = n_actions
                        
                        # Plot training history
                        st.markdown("### 📈 Training Progress")
                        fig_training = go.Figure()
                        fig_training.add_trace(go.Scatter(
                            x=list(range(1, episodes+1)),
                            y=history,
                            mode='lines+markers',
                            name='Average Reward',
                            line=dict(color='royalblue', width=2),
                            marker=dict(size=4)
                        ))
                        fig_training.update_layout(
                            title='Reward per Episode',
                            xaxis_title='Episode',
                            yaxis_title='Average Reward',
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig_training, use_container_width=True)
                        
                        # Display Q-Table
                        st.markdown("### 🗂️ Q-Table (Sample)")
                        q_table_df = pd.DataFrame(
                            agent.q_table,
                            columns=[f'Action {i}' for i in range(n_actions)],
                            index=[f'State {i}' for i in range(n_states)]
                        )
                        st.dataframe(q_table_df.head(10), use_container_width=True)
                        
                        # Statistik
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Max Reward", f"{max(history):.2f}")
                        with col2:
                            st.metric("Min Reward", f"{min(history):.2f}")
                        with col3:
                            st.metric("Final Reward", f"{history[-1]:.2f}")
                
                else:
                    st.info("👆 Klik tombol di atas untuk memulai training model")
            
            # ==================== TAB 3: REKOMENDASI ====================
            with tab3:
                st.markdown('<h2 class="sub-header">🎯 Sistem Rekomendasi Materi</h2>', unsafe_allow_html=True)
                
                if 'agent' in st.session_state:
                    agent = st.session_state['agent']
                    df_rl = st.session_state['df_rl']
                    
                    st.markdown("### 👨‍🎓 Input Data Siswa")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        math_score = st.slider("Math Score", 0, 100, 70)
                        reading_score = st.slider("Reading Score", 0, 100, 70)
                        writing_score = st.slider("Writing Score", 0, 100, 70)
                    
                    with col2:
                        gender = st.selectbox("Gender", df['gender'].unique())
                        grade_level = st.selectbox("Grade Level", sorted(df['grade_level'].unique()))
                        internet_access = st.selectbox("Internet Access", df['internet_access'].unique())
                    
                    with col3:
                        extra_activities = st.selectbox("Extra Activities", df['extra_activities'].unique())
                        study_hours = st.slider("Study Hours", 0.0, 5.0, 2.5, 0.1)
                    
                    if st.button("🎯 Dapatkan Rekomendasi", type="primary", use_container_width=True):
                        # Calculate average score
                        avg_score = (math_score + reading_score + writing_score) / 3
                        
                        # Determine performance category
                        if avg_score < 60:
                            performance = 'Low'
                            state = 0
                        elif avg_score < 75:
                            performance = 'Medium'
                            state = 1
                        elif avg_score < 90:
                            performance = 'High'
                            state = 2
                        else:
                            performance = 'Excellent'
                            state = 3
                        
                        # Get recommended action
                        recommended_action = agent.get_action(state, training=False)
                        
                        # Get Q-values for this state
                        q_values = agent.q_table[state]
                        
                        # Display results
                        st.markdown("---")
                        st.markdown("### 📋 Hasil Rekomendasi")
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Kategori Performa:** `{performance}`")
                            st.markdown(f"**Rata-rata Skor:** `{avg_score:.1f}`")
                            st.markdown(f"**Rekomendasi Aksi:** `Action {recommended_action}`")
                            
                            # Get learning materials
                            materials = get_learning_material_recommendations(performance, recommended_action)
                            
                            st.markdown("### 📚 Materi yang Direkomendasikan:")
                            for i, material in enumerate(materials, 1):
                                st.markdown(f"{i}. **{material}**")
                            
                            # Study plan
                            st.markdown("### 📅 Rencana Belajar:")
                            if recommended_action == 0:
                                st.info("🕐 **Intensitas Rendah**: 1-2 jam/hari, fokus pada pemahaman konsep dasar")
                            elif recommended_action == 1:
                                st.info("🕑 **Intensitas Sedang**: 2-3.5 jam/hari, kombinasi teori dan praktik")
                            else:
                                st.info("🕒 **Intensitas Tinggi**: 3.5-5 jam/hari, latihan intensif dan problem solving")
                        
                        with col2:
                            # Q-values visualization
                            fig_q = go.Figure(data=[
                                go.Bar(
                                    x=[f'Action {i}' for i in range(len(q_values))],
                                    y=q_values,
                                    marker_color=['red' if i != recommended_action else 'green' 
                                                 for i in range(len(q_values))],
                                    text=[f'{v:.2f}' for v in q_values],
                                    textposition='auto',
                                )
                            ])
                            fig_q.update_layout(
                                title='Q-Values per Action',
                                xaxis_title='Action',
                                yaxis_title='Q-Value',
                                showlegend=False
                            )
                            st.plotly_chart(fig_q, use_container_width=True)
                            
                            # Performance gauge
                            fig_gauge = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=avg_score,
                                domain={'x': [0, 1], 'y': [0, 1]},
                                title={'text': "Performance Score"},
                                gauge={
                                    'axis': {'range': [None, 100]},
                                    'bar': {'color': "darkblue"},
                                    'steps': [
                                        {'range': [0, 60], 'color': "lightcoral"},
                                        {'range': [60, 75], 'color': "lightyellow"},
                                        {'range': [75, 90], 'color': "lightgreen"},
                                        {'range': [90, 100], 'color': "lightblue"}
                                    ],
                                    'threshold': {
                                        'line': {'color': "red", 'width': 4},
                                        'thickness': 0.75,
                                        'value': 90
                                    }
                                }
                            ))
                            st.plotly_chart(fig_gauge, use_container_width=True)
                
                else:
                    st.warning("⚠️ Silakan lakukan training model terlebih dahulu di tab 'Training Model'")
            
            # ==================== TAB 4: ANALISIS HASIL ====================
            with tab4:
                st.markdown('<h2 class="sub-header">📈 Analisis Hasil & Evaluasi</h2>', unsafe_allow_html=True)
                
                if 'agent' in st.session_state:
                    agent = st.session_state['agent']
                    df_rl = st.session_state['df_rl']
                    
                    # Policy Evaluation
                    st.markdown("### 🎯 Evaluasi Policy")
                    
                    # Get optimal actions for each state
                    optimal_actions = []
                    for state in range(st.session_state['n_states']):
                        optimal_action = agent.get_action(state, training=False)
                        optimal_actions.append(optimal_action)
                    
                    # Create policy table
                    policy_df = pd.DataFrame({
                        'State': [f'State {i}' for i in range(st.session_state['n_states'])],
                        'Performance': ['Low', 'Medium', 'High', 'Excellent'][:st.session_state['n_states']],
                        'Optimal Action': [f'Action {a}' for a in optimal_actions],
                        'Max Q-Value': [agent.q_table[s].max() for s in range(st.session_state['n_states'])]
                    })
                    
                    st.dataframe(policy_df, use_container_width=True)
                    
                    # Visualize policy
                    fig_policy = px.bar(policy_df, x='State', y='Max Q-Value', 
                                       color='Optimal Action',
                                       title='Optimal Policy per State')
                    st.plotly_chart(fig_policy, use_container_width=True)
                    
                    # Heatmap Q-Table
                    st.markdown("### 🔥 Heatmap Q-Table")
                    fig_heatmap = px.imshow(
                        agent.q_table,
                        labels=dict(x="Action", y="State", color="Q-Value"),
                        x=[f'Action {i}' for i in range(st.session_state['n_actions'])],
                        y=[f'State {i}' for i in range(st.session_state['n_states'])],
                        color_continuous_scale='RdYlGn',
                        title='Q-Table Heatmap'
                    )
                    st.plotly_chart(fig_heatmap, use_container_width=True)
                    
                    # Performance metrics
                    st.markdown("### 📊 Metrik Performa")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        avg_q = agent.q_table.mean()
                        st.metric("Rata-rata Q-Value", f"{avg_q:.2f}")
                    
                    with col2:
                        max_q = agent.q_table.max()
                        st.metric("Max Q-Value", f"{max_q:.2f}")
                    
                    with col3:
                        min_q = agent.q_table.min()
                        st.metric("Min Q-Value", f"{min_q:.2f}")
                    
                    with col4:
                        std_q = agent.q_table.std()
                        st.metric("Std Q-Value", f"{std_q:.2f}")
                    
                    # Convergence analysis
                    if hasattr(agent, 'training_history') and agent.training_history:
                        st.markdown("### 📉 Analisis Konvergensi")
                        
                        history = agent.training_history
                        
                        # Calculate moving average
                        window = min(10, len(history))
                        moving_avg = pd.Series(history).rolling(window=window).mean()
                        
                        fig_conv = go.Figure()
                        fig_conv.add_trace(go.Scatter(
                            x=list(range(len(history))),
                            y=history,
                            mode='lines',
                            name='Reward',
                            line=dict(color='lightblue', width=1),
                            opacity=0.5
                        ))
                        fig_conv.add_trace(go.Scatter(
                            x=list(range(len(moving_avg))),
                            y=moving_avg,
                            mode='lines',
                            name='Moving Average',
                            line=dict(color='darkblue', width=3)
                        ))
                        fig_conv.update_layout(
                            title='Training Convergence',
                            xaxis_title='Episode',
                            yaxis_title='Average Reward',
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig_conv, use_container_width=True)
                
                else:
                    st.warning("⚠️ Silakan lakukan training model terlebih dahulu di tab 'Training Model'")
            
            # ==================== TAB 5: PROFIL SISWA ====================
            with tab5:
                st.markdown('<h2 class="sub-header">👤 Profil & Detail Siswa</h2>', unsafe_allow_html=True)
                
                # Search student
                student_id = st.selectbox("Pilih ID Siswa", df['student_id'].values)
                
                if student_id:
                    student = df[df['student_id'] == student_id].iloc[0]
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("### 📝 Informasi Dasar")
                        st.markdown(f"**ID:** {student['student_id']}")
                        st.markdown(f"**Nama:** {student['name']}")
                        st.markdown(f"**Gender:** {student['gender']}")
                        st.markdown(f"**Usia:** {student['age']} tahun")
                        st.markdown(f"**Tingkat:** {student['grade_level']}")
                        st.markdown(f"**Hasil:** {student['final_result']}")
                        
                        st.markdown("### 🏫 Informasi Akademik")
                        st.markdown(f"**Pendidikan Orang Tua:** {student['parent_education']}")
                        st.markdown(f"**Internet Access:** {student['internet_access']}")
                        st.markdown(f"**Tipe Makan:** {student['lunch_type']}")
                        st.markdown(f"**Aktivitas Ekstra:** {student['extra_activities']}")
                        st.markdown(f"**Jam Belajar:** {student['study_hours']:.2f} jam/hari")
                        st.markdown(f"**Tingkat Kehadiran:** {student['attendance_rate']:.1f}%")
                    
                    with col2:
                        # Scores radar chart
                        fig_radar = go.Figure()
                        
                        categories = ['Math', 'Reading', 'Writing', 'Study Hours (x10)', 'Attendance']
                        values = [
                            student['math_score'],
                            student['reading_score'],
                            student['writing_score'],
                            student['study_hours'] * 10,
                            student['attendance_rate']
                        ]
                        
                        fig_radar.add_trace(go.Scatterpolar(
                            r=values,
                            theta=categories,
                            fill='toself',
                            name=student['name']
                        ))
                        
                        fig_radar.update_layout(
                            polar=dict(
                                radialaxis=dict(
                                    visible=True,
                                    range=[0, 100]
                                )
                            ),
                            showlegend=False,
                            title='Profil Akademik Siswa'
                        )
                        st.plotly_chart(fig_radar, use_container_width=True)
                        
                        # Score comparison
                        scores_data = pd.DataFrame({
                            'Mata Pelajaran': ['Math', 'Reading', 'Writing'],
                            'Skor': [student['math_score'], student['reading_score'], student['writing_score']],
                            'Rata-rata Kelas': [df['math_score'].mean(), df['reading_score'].mean(), df['writing_score'].mean()]
                        })
                        
                        fig_comp = go.Figure()
                        fig_comp.add_trace(go.Bar(
                            x=scores_data['Mata Pelajaran'],
                            y=scores_data['Skor'],
                            name='Skor Siswa',
                            marker_color='lightblue'
                        ))
                        fig_comp.add_trace(go.Bar(
                            x=scores_data['Mata Pelajaran'],
                            y=scores_data['Rata-rata Kelas'],
                            name='Rata-rata Kelas',
                            marker_color='lightcoral'
                        ))
                        fig_comp.update_layout(
                            title='Perbandingan Skor dengan Rata-rata Kelas',
                            barmode='group'
                        )
                        st.plotly_chart(fig_comp, use_container_width=True)
                    
                    # Recommendations for this student
                    if 'agent' in st.session_state:
                        st.markdown("### 🎯 Rekomendasi untuk Siswa Ini")
                        
                        avg_score = student['avg_score']
                        if avg_score < 60:
                            performance = 'Low'
                            state = 0
                        elif avg_score < 75:
                            performance = 'Medium'
                            state = 1
                        elif avg_score < 90:
                            performance = 'High'
                            state = 2
                        else:
                            performance = 'Excellent'
                            state = 3
                        
                        agent = st.session_state['agent']
                        recommended_action = agent.get_action(state, training=False)
                        materials = get_learning_material_recommendations(performance, recommended_action)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"**Kategori Performa:** {performance}")
                            st.info(f"**Recommended Action:** Action {recommended_action}")
                        
                        with col2:
                            st.success("**Materi yang Direkomendasikan:**")
                            for material in materials:
                                st.write(f"• {material}")
        
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan: {str(e)}")
            st.exception(e)
    
    else:
        # Welcome screen
        st.markdown("""
        <div style='text-align: center; padding: 50px;'>
            <h2>👋 Selamat Datang!</h2>
            <p style='font-size: 1.2rem;'>
                Sistem Rekomendasi E-Learning berbasis Reinforcement Learning<br>
                menggunakan algoritma Q-Learning untuk personalisasi materi pembelajaran
            </p>
            <br>
            <p>📂 Silakan upload file <b>student_info.csv</b> di sidebar untuk memulai</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature highlights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='metric-card'>
                <h3>🤖 Machine Learning</h3>
                <p>Menggunakan Q-Learning untuk rekomendasi adaptif</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='metric-card'>
                <h3>📊 Analisis Data</h3>
                <p>Visualisasi interaktif dan insight mendalam</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='metric-card'>
                <h3>🎯 Personalisasi</h3>
                <p>Rekomendasi materi sesuai kebutuhan individu</p>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Developed by Kelompo 1 | Metode Penelitian | 2025</p>
        <p>📚 Sistem Rekomendasi E-Learning Berbasis Reinforcement Learning</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
