# AICup2023-No-Flask



## Overview

This is a fork of [AICup2023](https://github.com/AI-Cup-Kernel) That prepared for Reinforcement Learning or learn with
Genetic Algorithm. I remove all flask dependencies to make a complete game round faster
and easily develop RL algorithms.

## How to run

- [ ] Simply run `main.py` for running the whole game:
    ```
    python main.py
    ```
- [ ] Or run `main.py` with flag `-m map1.json` for running the whole game with selected map:
  ```
  python main.py -m map1.json
  ```
- [ ] You can change clients code on 'player0', 'player1', 'player2' folder
    ```
    ls /player0/
    - > initialize.py (Don't change this one. It's for connecting to kernel)
    - > main.py (write your algorithm here)
    ```
    ```
    Write your enemy algorithm in /player1/main.py and /player2/main.py
    ```
    As you know we have two methods to develop our code: `initializer` & `turn` on each client for two
    main phases of the game.

## If you have any problem

- [ ] Simply contact to me:
  - Telegram : [vahid](t.me/haj_vahid)
  - Discord: I am available on [Geek SQ](https://discord.gg/5PjQVd55) server
  
***
## Authors and acknowledgment
Our team in this contest:
- Vahid Ghafourian
- Mojtaba khanloo
- Zahra Nafarieh

## License
GNU GPL v3.0

## Project status
This project will update until the contest end
