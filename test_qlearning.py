"""
Script untuk testing Q-Learning Agent tanpa interface Streamlit
Gunakan script ini untuk memverifikasi bahwa algoritma berjalan dengan baik
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class QLearningAgent:
    def __init__(self, n_states, n_actions, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.n_states = n_states
        self.n_actions = n_actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = np.zeros((n_states, n_actions))
        self.training_history = []
        
    def get_action(self, state, training=True):
        if training and np.random.random() < self.epsilon:
            return np.random.randint(0, self.n_actions)
        else:
            return np.argmax(self.q_table[state])
    
    def update_q_value(self, state, action, reward, next_state):
        current_q = self.q_table[state, action]
        max_next_q = np.max(self.q_table[next_state])
        new_q = current_q + self.lr * (reward + self.gamma * max_next_q - current_q)
        self.q_table[state, action] = new_q
        
    def train(self, states, actions, rewards, next_states, episodes=100):
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
            
            if (episode + 1) % 10 == 0:
                print(f"Episode {episode + 1}/{episodes} - Avg Reward: {avg_reward:.4f}")
        
        return self.training_history

def prepare_data(csv_file):
    """Memuat dan memproses data"""
    print("Loading data...")
    df = pd.read_csv(csv_file)
    
    # Encoding
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
    
    # Calculate average score
    df['avg_score'] = (df['math_score'] + df['reading_score'] + df['writing_score']) / 3
    
    # Categorize performance (state)
    df['performance_category'] = pd.cut(df['avg_score'], 
                                        bins=[0, 60, 75, 90, 100], 
                                        labels=['Low', 'Medium', 'High', 'Excellent'])
    
    # Categorize study hours (action)
    df['study_hours_category'] = pd.cut(df['study_hours'], 
                                        bins=[0, 2, 3.5, 5], 
                                        labels=['Low', 'Medium', 'High'])
    
    # State
    df['state'] = df['performance_category'].astype('category').cat.codes
    
    # Action
    df['action'] = df['study_hours_category'].astype('category').cat.codes
    
    # Reward
    df['reward'] = df['final_result_encoded'] * 10 - 5
    
    # Next state
    df['next_state'] = df['state'].shift(-1).fillna(df['state'].iloc[-1]).astype(int)
    
    return df

def test_recommendation(agent, state, performance_level):
    """Test rekomendasi untuk state tertentu"""
    action = agent.get_action(state, training=False)
    q_values = agent.q_table[state]
    
    print(f"\n{'='*50}")
    print(f"Test Rekomendasi - Performance: {performance_level}")
    print(f"{'='*50}")
    print(f"State: {state}")
    print(f"Recommended Action: {action}")
    print(f"Q-Values: {q_values}")
    print(f"Confidence: {q_values[action]:.4f}")
    
    # Material recommendations
    materials = {
        'Low': ['Materi Dasar', 'Video Tutorial', 'Quiz Dasar'],
        'Medium': ['Materi Menengah', 'Problem Solving', 'Studi Kasus'],
        'High': ['Materi Lanjut', 'Applied Topics', 'Competition Prep'],
        'Excellent': ['Olimpiade', 'Research', 'Advanced Topics']
    }
    
    print(f"\nMateri yang Direkomendasikan:")
    for i, mat in enumerate(materials[performance_level], 1):
        print(f"  {i}. {mat}")
    
    study_plan = ['1-2 jam/hari (Intensitas Rendah)',
                  '2-3.5 jam/hari (Intensitas Sedang)',
                  '3.5-5 jam/hari (Intensitas Tinggi)']
    print(f"\nRencana Belajar: {study_plan[action]}")

def main():
    print("="*60)
    print("Q-LEARNING E-LEARNING RECOMMENDATION SYSTEM - TEST")
    print("="*60)
    
    # Load data
    df = prepare_data('student_info.csv')
    print(f"\n✓ Data loaded: {len(df)} records")
    
    # Get states and actions
    n_states = df['state'].nunique()
    n_actions = df['action'].nunique()
    
    print(f"✓ States: {n_states}")
    print(f"✓ Actions: {n_actions}")
    
    # Prepare training data
    states = df['state'].values
    actions = df['action'].values
    rewards = df['reward'].values
    next_states = df['next_state'].values
    
    print(f"\n{'='*60}")
    print("Training Q-Learning Agent...")
    print(f"{'='*60}")
    
    # Initialize and train agent
    agent = QLearningAgent(
        n_states=n_states,
        n_actions=n_actions,
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=0.1
    )
    
    history = agent.train(states, actions, rewards, next_states, episodes=100)
    
    print(f"\n✓ Training completed!")
    print(f"  - Initial Reward: {history[0]:.4f}")
    print(f"  - Final Reward: {history[-1]:.4f}")
    print(f"  - Improvement: {((history[-1] - history[0]) / abs(history[0]) * 100):.2f}%")
    
    # Display Q-Table
    print(f"\n{'='*60}")
    print("Q-Table Summary")
    print(f"{'='*60}")
    print(f"Shape: {agent.q_table.shape}")
    print(f"Mean Q-Value: {agent.q_table.mean():.4f}")
    print(f"Max Q-Value: {agent.q_table.max():.4f}")
    print(f"Min Q-Value: {agent.q_table.min():.4f}")
    
    print("\nQ-Table:")
    print(pd.DataFrame(
        agent.q_table,
        columns=[f'Action {i}' for i in range(n_actions)],
        index=[f'State {i}' for i in range(n_states)]
    ).round(4))
    
    # Test recommendations
    print(f"\n{'='*60}")
    print("Testing Recommendations")
    print(f"{'='*60}")
    
    performance_levels = ['Low', 'Medium', 'High', 'Excellent']
    for state in range(min(n_states, 4)):
        test_recommendation(agent, state, performance_levels[state])
    
    # Final statistics
    print(f"\n{'='*60}")
    print("Summary Statistics")
    print(f"{'='*60}")
    
    print(f"\nDataset Statistics:")
    print(f"  - Total Students: {len(df)}")
    print(f"  - Pass Rate: {(df['final_result'] == 'Pass').sum() / len(df) * 100:.2f}%")
    print(f"  - Avg Score: {df['avg_score'].mean():.2f}")
    print(f"  - Avg Study Hours: {df['study_hours'].mean():.2f}")
    
    print(f"\nPerformance Distribution:")
    print(df['performance_category'].value_counts())
    
    print(f"\nStudy Hours Distribution:")
    print(df['study_hours_category'].value_counts())
    
    print(f"\n{'='*60}")
    print("Test Completed Successfully! ✓")
    print(f"{'='*60}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
