# 📖 Dokumentasi Teknis

## Arsitektur Sistem

### 1. Struktur Kelas QLearningAgent

```python
class QLearningAgent:
    """
    Agent Q-Learning untuk sistem rekomendasi e-learning
    
    Attributes:
        n_states (int): Jumlah state yang mungkin
        n_actions (int): Jumlah action yang mungkin
        lr (float): Learning rate (α)
        gamma (float): Discount factor (γ)
        epsilon (float): Exploration rate (ε)
        q_table (numpy.ndarray): Q-table untuk menyimpan Q-values
        training_history (list): History reward selama training
    """
```

#### Methods:

**`__init__(n_states, n_actions, learning_rate, discount_factor, epsilon)`**
- Inisialisasi agent dengan parameter yang ditentukan
- Membuat Q-table dengan nilai awal 0

**`get_action(state, training=True)`**
- Memilih action menggunakan epsilon-greedy policy
- Return: action index (int)

**`update_q_value(state, action, reward, next_state)`**
- Update Q-value menggunakan Q-Learning equation
- Formula: Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]

**`train(states, actions, rewards, next_states, episodes)`**
- Melatih agent dengan dataset yang diberikan
- Return: training_history (list of average rewards)

## State Space

### Definisi State
State merepresentasikan kategori performa siswa berdasarkan rata-rata nilai:

| State | Performance | Score Range | Description |
|-------|------------|-------------|-------------|
| 0 | Low | 0 - 60 | Performa rendah, butuh materi dasar |
| 1 | Medium | 60 - 75 | Performa sedang, butuh penguatan |
| 2 | High | 75 - 90 | Performa tinggi, siap materi lanjut |
| 3 | Excellent | 90 - 100 | Performa excellent, siap materi olimpiade |

### Fitur State (Extended)
Meskipun state dikategorikan berdasarkan performa, sistem juga mempertimbangkan:
- Gender (Male/Female/Other)
- Grade Level (9-12)
- Internet Access (Yes/No)
- Extra Activities (Yes/No)
- Parent Education Level

## Action Space

### Definisi Action
Action merepresentasikan rekomendasi intensitas belajar:

| Action | Intensity | Hours/Day | Target Students |
|--------|-----------|-----------|----------------|
| 0 | Low | 1-2 | Siswa dengan beban belajar tinggi atau nilai rendah |
| 1 | Medium | 2-3.5 | Siswa dengan performa seimbang |
| 2 | High | 3.5-5 | Siswa berprestasi tinggi atau persiapan kompetisi |

### Materi per Action

#### Action 0 - Low Intensity
- Fokus: Pemahaman konsep dasar
- Metode: Video tutorial interaktif
- Evaluasi: Quiz sederhana
- Target: Membangun fondasi yang kuat

#### Action 1 - Medium Intensity
- Fokus: Aplikasi konsep
- Metode: Problem solving dan studi kasus
- Evaluasi: Ujian komprehensi
- Target: Meningkatkan pemahaman mendalam

#### Action 2 - High Intensity
- Fokus: Materi advanced dan kompetisi
- Metode: Research dan proyek
- Evaluasi: Presentasi dan paper
- Target: Persiapan olimpiade/kompetisi

## Reward Function

### Formula Reward
```python
if final_result == "Pass":
    reward = +5
else:
    reward = -5
```

### Rationale
- **+5 (Pass)**: Siswa berhasil mencapai standar minimal
- **-5 (Fail)**: Siswa tidak mencapai standar, perlu perbaikan strategi

### Future Improvements
Reward bisa diperluas dengan:
- Skor improvement: +bonus jika nilai meningkat
- Time efficiency: +bonus jika target tercapai lebih cepat
- Engagement: +bonus untuk aktivitas dan kehadiran tinggi

## Algoritma Q-Learning

### Update Rule
```
Q(s,a) ← Q(s,a) + α[r + γ max Q(s',a') - Q(s,a)]
                        a'
```

### Parameter Explanation

**Learning Rate (α)**
- Range: 0 < α ≤ 1
- Recommended: 0.1
- Effect:
  - α tinggi: Belajar cepat tapi tidak stabil
  - α rendah: Belajar lambat tapi lebih stabil

**Discount Factor (γ)**
- Range: 0 ≤ γ ≤ 1
- Recommended: 0.9
- Effect:
  - γ = 0: Hanya peduli reward immediate
  - γ = 1: Pertimbangkan semua future rewards sama

**Epsilon (ε)**
- Range: 0 ≤ ε ≤ 1
- Recommended: 0.1
- Effect:
  - ε tinggi: Lebih banyak eksplorasi
  - ε rendah: Lebih banyak eksploitasi

## Data Processing Pipeline

### 1. Load Data
```python
df = pd.read_csv('student_info.csv')
```

### 2. Encoding Categorical Features
```python
# Gender, Education, Internet Access, etc.
le = LabelEncoder()
df['feature_encoded'] = le.fit_transform(df['feature'])
```

### 3. Feature Engineering
```python
# Average Score
df['avg_score'] = (math + reading + writing) / 3

# Performance Category
df['performance_category'] = pd.cut(avg_score, bins, labels)

# State Encoding
df['state'] = performance_category.astype('category').cat.codes
```

### 4. Action & Reward
```python
# Action dari study hours
df['action'] = study_hours_category.astype('category').cat.codes

# Reward dari final result
df['reward'] = (final_result_encoded * 10) - 5
```

### 5. Next State
```python
df['next_state'] = df['state'].shift(-1).fillna(last_state)
```

## API Functions

### Data Loading
```python
@st.cache_data
def load_and_preprocess_data(file_path):
    """
    Load CSV dan preprocessing
    Returns: df, encoders
    """
```

### RL Data Preparation
```python
def prepare_rl_data(df):
    """
    Convert dataframe ke format RL
    Returns: df dengan state, action, reward
    """
```

### Recommendation
```python
def get_learning_material_recommendations(performance, action_type):
    """
    Generate daftar materi berdasarkan performa dan action
    Returns: list of materials
    """
```

## Streamlit Components

### Tabs Organization
1. **Eksplorasi Data**: EDA dan visualisasi
2. **Training Model**: Interface untuk training
3. **Rekomendasi**: Input siswa dan hasil rekomendasi
4. **Analisis Hasil**: Evaluasi policy dan Q-table
5. **Profil Siswa**: Detail individual student

### Visualization Tools
- **Plotly Express**: Charts interaktif
- **Plotly Graph Objects**: Custom visualizations
- **Pandas**: Data display dan manipulation

## Performance Optimization

### Caching Strategy
```python
@st.cache_data  # Cache data loading
def load_and_preprocess_data(file_path):
    ...

# Session state untuk agent
st.session_state['agent'] = agent
```

### Memory Management
- Use numpy arrays untuk Q-table (efisien)
- Limit visualization data points jika dataset besar
- Clear cache jika perlu: `st.cache_data.clear()`

## Testing & Validation

### Unit Testing
```bash
python test_qlearning.py
```

### Integration Testing
1. Load data
2. Train agent
3. Generate recommendations
4. Verify Q-values reasonable

### Performance Metrics
- Training convergence
- Q-value stability
- Recommendation consistency
- User satisfaction (manual)

## Deployment Options

### Local Development
```bash
streamlit run elearning_recommendation_app.py
```

### Cloud Deployment

**Streamlit Cloud:**
1. Push to GitHub
2. Connect repository
3. Deploy automatic

**Heroku:**
```bash
heroku create app-name
git push heroku main
```

**Docker:**
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD streamlit run elearning_recommendation_app.py
```

## Security Considerations

### Data Privacy
- Tidak menyimpan data siswa permanen
- Session-based storage
- Clear cache saat logout

### Input Validation
- Validate CSV format
- Check data types
- Handle missing values
- Sanitize user inputs

## Future Enhancements

### 1. Deep Q-Learning (DQN)
- Neural network sebagai Q-function
- Better generalization
- Handle continuous state space

### 2. Multi-Armed Bandit
- Contextual bandits
- Online learning
- Real-time adaptation

### 3. Advanced Features
- Collaborative filtering integration
- Content-based filtering hybrid
- User feedback loop
- A/B testing framework

### 4. Analytics Dashboard
- Real-time monitoring
- Performance analytics
- Student progress tracking
- Intervention alerts

## Code Style & Standards

### Python Style Guide
- Follow PEP 8
- Use type hints where applicable
- Comprehensive docstrings
- Meaningful variable names

### Example:
```python
def calculate_reward(final_result: str) -> float:
    """
    Calculate reward based on student's final result.
    
    Args:
        final_result (str): Student's final result ('Pass' or 'Fail')
    
    Returns:
        float: Reward value (+5 for Pass, -5 for Fail)
    """
    return 5.0 if final_result == "Pass" else -5.0
```

## Troubleshooting Guide

### Common Issues

**Issue 1: Q-values tidak konvergen**
- Solution: Turunkan learning rate
- Solution: Tingkatkan jumlah episodes
- Solution: Adjust discount factor

**Issue 2: Rekomendasi tidak masuk akal**
- Solution: Check reward function
- Solution: Verify state-action mapping
- Solution: Increase training data

**Issue 3: Aplikasi lambat**
- Solution: Reduce visualization complexity
- Solution: Use sampling untuk large datasets
- Solution: Optimize caching

## References & Resources

### Academic Papers
1. Watkins & Dayan (1992) - Q-Learning
2. Mnih et al. (2015) - Deep Q-Networks
3. Sutton & Barto (2018) - Reinforcement Learning: An Introduction

### Code Libraries
- Streamlit: https://streamlit.io/
- Scikit-learn: https://scikit-learn.org/
- Plotly: https://plotly.com/python/

### Tutorials
- Q-Learning Tutorial: https://www.learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/
- Streamlit Tutorial: https://docs.streamlit.io/

## Contact & Support

Untuk pertanyaan teknis:
- Email: [your-email]
- GitHub Issues: [repo-url]
- Documentation: [docs-url]

---

**Last Updated:** December 2024
**Version:** 1.0.0
**Author:** Siti Rahma Alia
