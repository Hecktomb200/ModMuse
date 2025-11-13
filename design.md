# ModMuse 🎮
**AI-Powered Mod Recommendation Generator**

---

## Project Summary

**ModMuse** is an AI-powered recommendation system that helps gamers discover new ways to enjoy their favorite titles.  
By entering a natural-language prompt such as _“I want a hardcore survival experience in Skyrim”_, ModMuse intelligently generates a curated list of compatible mods that deliver that experience.

The system uses AI to:
- Parse the player’s intent
- Match it with mod metadata (genre, theme, mechanics, compatibility)
- Filter and rank mods for the best combined experience

Ultimately, ModMuse aims to support multiple games and allow community-driven updates to mod data.

---

## Purpose and Goals

**Purpose:** Streamline the process of finding compatible and theme-consistent mods using natural language.

**Goals:**
- Parse user intent with AI (e.g., GPT or similar model)
- Query a mod metadata database (tags, categories, dependencies)
- Filter out incompatible or redundant mods
- Provide a formatted recommendation list with relevance scores and compatibility indicators
- (Optional) Visualize mod compatibility networks

---

## Estimated Timeline

| Date            | Goal                                                                        |
| --------------- | --------------------------------------------------------------------------- |
| **Part 1**  | Create GitHub repository, upload `README.md`, `design.md`                   |
| **Part 2**  | Set up backend skeleton (FastAPI or Node.js)                                |
| **Part 3**  | Build and seed initial mod/game database                                    |
| **Part 4**  | Integrate AI model (OpenAI API or local LLM)                                |
| **Part 5**  | Connect backend and frontend for prompt submission                          |
| **Part 6**  | Implement filtering and compatibility logic                                 |
| **Part 7**  | Polish UI, add styling, prepare demo and presentation                       |

---

## Entity-Relationship Diagram (ERD)

```mermaid
erDiagram

    %% --- Relationships ---
    GAME ||--o{ MOD : has

    MOD ||--o{ MOD_TAG : has_tag
    TAG ||--o{ MOD_TAG : categorizes

    MOD ||--o{ DEPENDENCY : depends_on
    MOD ||--o{ INCOMPATIBILITY : conflicts_with

    PROMPT ||--o{ RECOMMENDATION : generates
    MOD ||--o{ RECOMMENDATION : recommended

    %% --- Entities ---

    GAME {
        int game_id PK
        string name
        string genre
        string engine
        string platform
    }

    MOD {
        int mod_id PK
        string name
        string description
        string source_url
        string version
        int game_id
    }

    TAG {
        int tag_id PK
        string name
    }

    MOD_TAG {
        int mod_id PK
        int tag_id PK
    }

    DEPENDENCY {
        int mod_id PK
        int depends_on_id PK
        string note
    }

    INCOMPATIBILITY {
        int mod_a_id PK
        int mod_b_id PK
        string reason
    }

    PROMPT {
        int prompt_id PK
        string user_prompt
        datetime created_at
        string extracted_keywords
        string model_version
    }

    RECOMMENDATION {
        int rec_id PK
        int prompt_id
        int mod_id
        float relevance_score
        int rank_order
    }
```

## System Design Overview

```mermaid
graph TD

    %% --- Frontend Layer ---
    subgraph Frontend
        A[React / Vue App<br>• Prompt Input<br>• Mod Display UI]
    end

    %% --- Backend Layer ---
    subgraph Backend
        B[API Server FastAPI / Node.js<br>• Handles requests<br>• Validates input<br>• Calls AI & DB]
        C[AI Prompt Processor<br>• Analyzes user intent<br>• Generates mod keywords]
        D[Database<br>Postgres / MySQL<br>• Stores mods, tags, compatibility]
    end

    %% --- Data Flow ---
    A -->|Submit Prompt| B
    B -->|Send Prompt →| C
    C -->|Return Mod Keywords| B
    B -->|Query Mods| D
    D -->|Return Mod Data| B
    B -->|Return JSON Response| A

    %% --- Optional Layers ---
    subgraph Optional_Components [Optional Components]
        E[(Vector DB / Semantic Search)]
    end
    C -.->|Embed Search| E
    E -.->|Relevant Mods| B

