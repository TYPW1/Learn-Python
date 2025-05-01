import streamlit as st
import random
import time
import pandas as pd
import numpy as np
import base64

# Set page config
st.set_page_config(
    page_title="Pixel Brawlers",
    page_icon="🥊",
    layout="wide"
)

# Initialize session state variables
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'player_character' not in st.session_state:
    st.session_state.player_character = None
if 'cpu_character' not in st.session_state:
    st.session_state.cpu_character = None
if 'player_health' not in st.session_state:
    st.session_state.player_health = 100
if 'cpu_health' not in st.session_state:
    st.session_state.cpu_health = 100
if 'battle_log' not in st.session_state:
    st.session_state.battle_log = []
if 'turn' not in st.session_state:
    st.session_state.turn = 'player'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None

# Character data
characters = {
    "Blaze": {
        "health": 100,
        "attack": 20,
        "defense": 15,
        "speed": 18,
        "color": "red",
        "special_move": "Fire Tornado",
        "special_damage": 35,
        "image": "🔥👊",
        "description": "A fierce fighter with fire-based attacks. High damage, moderate defense."
    },
    "Shadow": {
        "health": 90,
        "attack": 25,
        "defense": 10,
        "speed": 25, 
        "color": "purple",
        "special_move": "Void Strike",
        "special_damage": 40,
        "image": "⚡🥷",
        "description": "A nimble assassin who strikes from darkness. High speed, high attack."
    },
    "Guardian": {
        "health": 120,
        "attack": 15,
        "defense": 25,
        "speed": 10,
        "color": "blue",
        "special_move": "Shield Bash",
        "special_damage": 30,
        "image": "🛡️🪖",
        "description": "A tank-like warrior with incredible defense. High health, low speed."
    },
    "Mystic": {
        "health": 85,
        "attack": 28,
        "defense": 12,
        "speed": 20,
        "color": "teal",
        "special_move": "Arcane Blast",
        "special_damage": 45,
        "image": "✨🧙",
        "description": "A magical fighter with powerful spells. Very high special attack damage."
    }
}

# Custom CSS
def local_css():
    st.markdown("""
    <style>
    .main {
        background-color: #121212;
        color: white;
    }
    .character-card {
        background-color: #2e2e2e;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        text-align: center;
        transition: transform 0.3s;
    }
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .character-image {
        font-size: 5rem;
        margin-bottom: 10px;
    }
    .health-bar-container {
        width: 100%;
        background-color: #444;
        border-radius: 5px;
        margin: 10px 0;
        height: 25px;
    }
    .health-bar {
        height: 25px;
        border-radius: 5px;
        transition: width 0.5s ease-in-out;
    }
    .battle-log {
        background-color: #1e1e1e;
        border-radius: 5px; 
        padding: 10px;
        height: 200px;
        overflow-y: auto;
        margin-top: 20px;
    }
    .log-entry {
        margin: 5px 0;
        padding: 3px;
        border-bottom: 1px solid #333;
    }
    .game-title {
        font-size: 4rem;
        text-align: center;
        margin-bottom: 20px;
        background: linear-gradient(45deg, #f06, #0cf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .btn-special {
        background: linear-gradient(45deg, #f06, #0cf);
        border: none;
        color: white;
        padding: 10px 24px;
        font-weight: bold;
        border-radius: 5px;
    }
    .btn-attack {
        background-color: #f55;
        border: none;
        color: white;
        padding: 10px 24px;
        font-weight: bold;
        border-radius: 5px;
    }
    .btn-defend {
        background-color: #55f;
        border: none;
        color: white;
        padding: 10px 24px;
        font-weight: bold;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Apply CSS
local_css()

# Game mechanics functions
def attack(attacker, defender, is_special=False):
    if is_special:
        base_damage = characters[attacker]["special_damage"]
        move_name = characters[attacker]["special_move"]
        hit_chance = 0.7  # Special moves have lower hit chance
    else:
        base_damage = characters[attacker]["attack"]
        move_name = "Attack"
        hit_chance = 0.9
    
    # Random factors
    hit_roll = random.random()
    if hit_roll > hit_chance:
        return 0, f"{attacker}'s {move_name} missed!"
    
    # Calculate damage with some randomness and defense reduction
    damage_multiplier = random.uniform(0.8, 1.2)
    defense_reduction = characters[defender]["defense"] / 100
    damage = max(1, int(base_damage * damage_multiplier * (1 - defense_reduction)))
    
    if is_special:
        message = f"{attacker} used {move_name} dealing {damage} damage!"
    else:
        message = f"{attacker} attacked for {damage} damage!"
    
    return damage, message

def defend(character):
    defense_boost = int(characters[character]["defense"] * 0.5)
    return defense_boost, f"{character} took a defensive stance (+{defense_boost} defense)!"

def cpu_turn():
    # AI decision making
    if st.session_state.cpu_health < 30 and random.random() > 0.5:
        # CPU is low on health, higher chance to defend
        defense_boost, message = defend(st.session_state.cpu_character)
        st.session_state.cpu_defense_boost = defense_boost
        st.session_state.battle_log.append({"time": time.time(), "message": message, "type": "cpu"})
    elif random.random() > 0.7:
        # 30% chance for special attack if health is good
        damage, message = attack(st.session_state.cpu_character, st.session_state.player_character, is_special=True)
        st.session_state.player_health = max(0, st.session_state.player_health - damage)
        st.session_state.battle_log.append({"time": time.time(), "message": message, "type": "cpu"})
    else:
        # Regular attack
        damage, message = attack(st.session_state.cpu_character, st.session_state.player_character)
        st.session_state.player_health = max(0, st.session_state.player_health - damage)
        st.session_state.battle_log.append({"time": time.time(), "message": message, "type": "cpu"})
    
    # Check if game is over after CPU turn
    check_game_over()
    
    if not st.session_state.game_over:
        st.session_state.turn = 'player'

def check_game_over():
    if st.session_state.player_health <= 0:
        st.session_state.game_over = True
        st.session_state.winner = "CPU"
        st.session_state.battle_log.append({"time": time.time(), "message": f"Game Over! {st.session_state.cpu_character} wins!", "type": "system"})
    elif st.session_state.cpu_health <= 0:
        st.session_state.game_over = True
        st.session_state.winner = "Player"
        st.session_state.battle_log.append({"time": time.time(), "message": f"Game Over! {st.session_state.player_character} wins!", "type": "system"})

def reset_game():
    st.session_state.game_started = False
    st.session_state.player_character = None
    st.session_state.cpu_character = None
    st.session_state.player_health = 100
    st.session_state.cpu_health = 100
    st.session_state.battle_log = []
    st.session_state.turn = 'player'
    st.session_state.game_over = False
    st.session_state.winner = None

def player_select_character(character):
    st.session_state.player_character = character
    remaining_chars = [c for c in characters.keys() if c != character]
    st.session_state.cpu_character = random.choice(remaining_chars)
    st.session_state.player_health = characters[character]["health"]
    st.session_state.cpu_health = characters[st.session_state.cpu_character]["health"]
    st.session_state.game_started = True
    st.session_state.battle_log = []
    st.session_state.battle_log.append({"time": time.time(), "message": f"Battle begins! {character} vs {st.session_state.cpu_character}", "type": "system"})

# Main game UI
st.markdown('<h1 class="game-title">PIXEL BRAWLERS</h1>', unsafe_allow_html=True)

if not st.session_state.game_started:
    st.markdown("## Choose Your Fighter")
    
    cols = st.columns(len(characters))
    
    for i, (name, data) in enumerate(characters.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="character-card" style="border: 2px solid {data['color']}">
                <div class="character-image">{data['image']}</div>
                <h3>{name}</h3>
                <p><b>Health:</b> {data['health']}</p>
                <p><b>Attack:</b> {data['attack']}</p>
                <p><b>Defense:</b> {data['defense']}</p>
                <p><b>Speed:</b> {data['speed']}</p>
                <p><i>{data['description']}</i></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select {name}"):
                player_select_character(name)
                st.experimental_rerun()
else:
    # Battle screen
    player = st.session_state.player_character
    cpu = st.session_state.cpu_character
    
    # Character display and health bars
    col1, col2 = st.columns(2)
    
    with col1:
        # Player character
        player_data = characters[player]
        player_health_percent = (st.session_state.player_health / player_data["health"]) * 100
        
        st.markdown(f"""
        <div class="character-card" style="border: 2px solid {player_data['color']}">
            <h2>{player} (You)</h2>
            <div class="character-image">{player_data['image']}</div>
            <div class="health-bar-container">
                <div class="health-bar" style="width: {player_health_percent}%; background-color: {'green' if player_health_percent > 50 else 'orange' if player_health_percent > 20 else 'red'}"></div>
            </div>
            <p>Health: {st.session_state.player_health}/{player_data['health']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # CPU character
        cpu_data = characters[cpu]
        cpu_health_percent = (st.session_state.cpu_health / cpu_data["health"]) * 100
        
        st.markdown(f"""
        <div class="character-card" style="border: 2px solid {cpu_data['color']}">
            <h2>{cpu} (CPU)</h2>
            <div class="character-image">{cpu_data['image']}</div>
            <div class="health-bar-container">
                <div class="health-bar" style="width: {cpu_health_percent}%; background-color: {'green' if cpu_health_percent > 50 else 'orange' if cpu_health_percent > 20 else 'red'}"></div>
            </div>
            <p>Health: {st.session_state.cpu_health}/{cpu_data['health']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Battle log
    st.markdown("<div class='battle-log'>", unsafe_allow_html=True)
    for entry in reversed(st.session_state.battle_log[-10:]):
        message_style = ""
        if entry["type"] == "player":
            message_style = "color: #5ff;"
        elif entry["type"] == "cpu":
            message_style = "color: #f55;"
        elif entry["type"] == "system":
            message_style = "color: #ff5;"
        
        st.markdown(f"<div class='log-entry' style='{message_style}'>{entry['message']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Game controls
    if not st.session_state.game_over:
        if st.session_state.turn == 'player':
            st.markdown("## Your Turn")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Attack", key="attack_btn", use_container_width=True):
                    damage, message = attack(player, cpu)
                    st.session_state.cpu_health = max(0, st.session_state.cpu_health - damage)
                    st.session_state.battle_log.append({"time": time.time(), "message": message, "type": "player"})
                    check_game_over()
                    if not st.session_state.game_over:
                        st.session_state.turn = 'cpu'
                        st.experimental_rerun()
                    else:
                        st.experimental_rerun()
            
            with col2:
                if st.button("Special Attack", key="special_btn", use_container_width=True):
                    damage, message = attack(player, cpu, is_special=True)
                    st.session_state.cpu_health = max(0, st.session_state.cpu_health - damage)
                    st.session_state.battle_log.append({"time": time.time(), "message": message, "type": "player"})
                    check_game_over()
                    if not st.session_state.game_over:
                        st.session_state.turn = 'cpu'
                        st.experimental_rerun()
                    else:
                        st.experimental_rerun()
            
            with col3:
                if st.button("Defend", key="defend_btn", use_container_width=True):
                    defense_boost, message = defend(player)
                    st.session_state.player_health = min(characters[player]["health"], st.session_state.player_health + defense_boost)
                    st.session_state.battle_log.append({"time": time.time(), "message": message, "type": "player"})
                    st.session_state.turn = 'cpu'
                    st.experimental_rerun()
        
        else:  # CPU's turn
            st.markdown("## CPU's Turn")
            with st.spinner("CPU is thinking..."):
                time.sleep(1)  # Simulate CPU thinking
                cpu_turn()
                st.experimental_rerun()
    else:
        # Game over state
        if st.session_state.winner == "Player":
            st.success(f"Victory! {player} has defeated {cpu}!")
        else:
            st.error(f"Defeat! {cpu} has defeated {player}!")
        
        if st.button("Play Again"):
            reset_game()
            st.experimental_rerun()

# About section
with st.expander("Game Info"):
    st.markdown("""
    # About Pixel Brawlers
    
    A turn-based fighting game with different character classes, each with unique stats and special moves.
    
    ## How to Play
    1. Select your fighter from the available characters
    2. Take turns attacking, using special moves, or defending
    3. Reduce your opponent's health to zero to win
    
    ## Characters
    Each character has different stats:
    - **Health**: How much damage they can take
    - **Attack**: Base attack power
    - **Defense**: Reduces incoming damage
    - **Speed**: Determines who goes first (not used in current version)
    
    ## Special Moves
    Each character has a unique special move that deals more damage but has a lower chance to hit.
    """)
