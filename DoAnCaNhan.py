import asyncio
import platform
import pygame
import pygame.freetype
from collections import deque
import heapq
import time
import sys
import random
import math
import copy
from tkinter import Tk, messagebox, simpledialog

FPS = 5

SIM_APP_BACKGROUND_COLOR = (220, 230, 230)
SIM_CONTENT_BACKGROUND_COLOR = (200, 220, 220)
SIM_HEADER_BG_COLOR = (30, 70, 70)
SIM_TEXT_COLOR_DARK = (10, 50, 50)
SIM_TEXT_COLOR_LIGHT = (230, 245, 245)
SIM_TEXT_COLOR_ON_TILE = SIM_TEXT_COLOR_LIGHT

SIM_TILE_COLOR = (0, 128, 128)
SIM_TILE_EMPTY_COLOR = (160, 190, 190)
SIM_TILE_BORDER_COLOR = (0, 100, 100)
SIM_TILE_BORDER_WIDTH = 1
SIM_TILE_BORDER_RADIUS = 3

SIM_BUTTON_BG_COLOR = (20, 140, 140)
SIM_BUTTON_HOVER_COLOR = (30, 160, 160)
SIM_BUTTON_ACTIVE_COLOR = (10, 120, 120)
SIM_BUTTON_TEXT_COLOR = SIM_TEXT_COLOR_LIGHT
SIM_DISABLED_BUTTON_BG_COLOR = (130, 160, 160)

SIM_HIGHLIGHT_GREEN_CORRECT_POS = (60, 179, 113, 180)
SIM_HIGHLIGHT_FIXED_TILE_BG = (255, 182, 193, 150)
SIM_HIGHLIGHT_YELLOW_PO_ROW = (255, 255, 150, 128)
SIM_HIGHLIGHT_SOLVED_PUZZLE = (144, 238, 144, 180)
SIM_HIGHLIGHT_FOUND_GOAL_BORDER = (255, 215, 0)
SIM_HIGHLIGHT_AND_OR_FIXED_BORDER = (255, 69, 0)

SIM_GRID_SIZE = 3
SIM_DISPLAY_TILE_SIZE_PO = 25
SIM_DISPLAY_TILE_SIZE_NON_OBS = 20
SIM_DISPLAY_TILE_SIZE_AND_OR = 60

SIM_STANDARD_GOAL_STATE_LIST = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
SIM_STANDARD_GOAL_STATE_TUPLE = tuple(map(tuple, SIM_STANDARD_GOAL_STATE_LIST))
SIM_PARTIAL_OBSERVABLE_GOAL_FIXED_PART = [[1, 2, 3]]

SIM_TARGET_POSITIONS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 0: (2, 2)
}


def sim_find_zero_pos(state_list_or_tuple):
    for r in range(SIM_GRID_SIZE):
        for c in range(SIM_GRID_SIZE):
            if state_list_or_tuple[r][c] == 0: return (r, c)
    return None


def sim_get_tile_pos(state_list_or_tuple, tile_value):
    for r in range(SIM_GRID_SIZE):
        for c in range(SIM_GRID_SIZE):
            if state_list_or_tuple[r][c] == tile_value: return (r, c)
    return None


def sim_manhattan_distance(pos1, pos2):
    if pos1 is None or pos2 is None: return float('inf')
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def sim_get_valid_successors_standard(state_tuple):
    successors = []
    zero_pos = sim_find_zero_pos(state_tuple)
    if not zero_pos: return successors
    zero_r, zero_c = zero_pos
    possible_moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
    current_state_list = [list(row) for row in state_tuple]
    for dr, dc, action_name in possible_moves:
        next_zero_r, next_zero_c = zero_r + dr, zero_c + dc
        if 0 <= next_zero_r < SIM_GRID_SIZE and 0 <= next_zero_c < SIM_GRID_SIZE:
            new_state_list = copy.deepcopy(current_state_list)
            new_state_list[zero_r][zero_c], new_state_list[next_zero_r][next_zero_c] = new_state_list[next_zero_r][
                next_zero_c], new_state_list[zero_r][zero_c]
            successors.append({'action': action_name, 'state': tuple(map(tuple, new_state_list))})
    return successors


def sim_apply_action_standard(state_list, action_name):
    zero_pos = sim_find_zero_pos(state_list)
    if not zero_pos: return copy.deepcopy(state_list)
    zero_r, zero_c = zero_pos
    dr, dc = 0, 0
    if action_name == 'UP':
        dr = -1
    elif action_name == 'DOWN':
        dr = 1
    elif action_name == 'LEFT':
        dc = -1
    elif action_name == 'RIGHT':
        dc = 1
    else:
        return copy.deepcopy(state_list)
    next_zero_r, next_zero_c = zero_r + dr, zero_c + dc
    new_state = copy.deepcopy(state_list)
    if 0 <= next_zero_r < SIM_GRID_SIZE and 0 <= next_zero_c < SIM_GRID_SIZE:
        new_state[zero_r][zero_c], new_state[next_zero_r][next_zero_c] = new_state[next_zero_r][next_zero_c], \
            new_state[zero_r][zero_c]
    return new_state


def sim_generate_initial_states_standard_close(num_puzzles=1, root_shuffles=5, variation_shuffles=0):
    puzzles = []
    generated_tuples = set()
    for _ in range(num_puzzles * 3):
        if len(puzzles) >= num_puzzles: break
        current_state_tuple = SIM_STANDARD_GOAL_STATE_TUPLE
        total_shuffles = root_shuffles + random.randint(0, variation_shuffles)
        for _ in range(total_shuffles):
            successors = sim_get_valid_successors_standard(current_state_tuple)
            if not successors: break
            current_state_tuple = random.choice(successors)['state']
        if current_state_tuple not in generated_tuples:
            puzzles.append([list(row) for row in current_state_tuple])
            generated_tuples.add(current_state_tuple)
    while len(puzzles) < num_puzzles:
        if puzzles:
            base_for_fallback = tuple(map(tuple, puzzles[random.randint(0, len(puzzles) - 1)]))
            for _ in range(max(1, variation_shuffles if variation_shuffles > 0 else 1)):
                successors = sim_get_valid_successors_standard(base_for_fallback)
                if not successors: break
                base_for_fallback = random.choice(successors)['state']
            if base_for_fallback not in generated_tuples:
                puzzles.append([list(row) for row in base_for_fallback])
                generated_tuples.add(base_for_fallback)
            else:
                puzzles.append(copy.deepcopy(puzzles[0]))
        else:
            puzzles.append(copy.deepcopy(SIM_STANDARD_GOAL_STATE_LIST))
        if len(puzzles) >= num_puzzles: break
    return puzzles[:num_puzzles]


def sim_check_goal_state_standard(state_list): return state_list == SIM_STANDARD_GOAL_STATE_LIST


def sim_get_valid_successors_for_bfs_po(state_tuple):
    successors = []
    zero_r, zero_c = sim_find_zero_pos(state_tuple)
    possible_moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
    current_state_list = [list(row) for row in state_tuple]
    for dr, dc, action in possible_moves:
        next_zero_r, next_zero_c = zero_r + dr, zero_c + dc
        if 0 <= next_zero_r < SIM_GRID_SIZE and 0 <= next_zero_c < SIM_GRID_SIZE and next_zero_r != 0:
            new_state_list = copy.deepcopy(current_state_list)
            new_state_list[zero_r][zero_c], new_state_list[next_zero_r][next_zero_c] = \
                new_state_list[next_zero_r][next_zero_c], new_state_list[zero_r][zero_c]
            successors.append({'action': action, 'state': tuple(map(tuple, new_state_list))})
    return successors


def sim_apply_single_action_to_state_po(state_list, action):
    zero_pos = sim_find_zero_pos(state_list)
    if not zero_pos: return copy.deepcopy(state_list)
    zero_r, zero_c = zero_pos
    dr, dc = 0, 0
    if action == 'UP':
        dr, dc = -1, 0
    elif action == 'DOWN':
        dr, dc = 1, 0
    elif action == 'LEFT':
        dr, dc = 0, -1
    elif action == 'RIGHT':
        dr, dc = 0, 1
    else:
        return copy.deepcopy(state_list)

    next_zero_r, next_zero_c = zero_r + dr, zero_c + dc
    new_state = copy.deepcopy(state_list)
    if 0 <= next_zero_r < SIM_GRID_SIZE and 0 <= next_zero_c < SIM_GRID_SIZE and next_zero_r != 0:
        new_state[zero_r][zero_c], new_state[next_zero_r][next_zero_c] = \
            new_state[next_zero_r][next_zero_c], new_state[zero_r][zero_c]
    return new_state


def sim_generate_solvable_close_states_po(num_states=9, max_shuffles=6, min_shuffles=2):
    belief_set = []
    generated_states_tuples = set()
    for _ in range(num_states * 3):
        if len(belief_set) >= num_states: break
        current_state_tuple = SIM_STANDARD_GOAL_STATE_TUPLE
        num_shuffles = random.randint(min_shuffles, max_shuffles)
        for _ in range(num_shuffles):
            successors = sim_get_valid_successors_for_bfs_po(current_state_tuple)
            if not successors: break
            current_state_tuple = random.choice(successors)['state']

        current_state_list = [list(row) for row in current_state_tuple]
        if current_state_list[0] != SIM_PARTIAL_OBSERVABLE_GOAL_FIXED_PART[0]:
            fixed_top_row = copy.deepcopy(SIM_PARTIAL_OBSERVABLE_GOAL_FIXED_PART[0])
            remaining_numbers = [n for n in range(SIM_GRID_SIZE * SIM_GRID_SIZE) if n not in fixed_top_row]
            random.shuffle(remaining_numbers)
            current_state_list = [fixed_top_row,
                                  remaining_numbers[0:SIM_GRID_SIZE],
                                  remaining_numbers[SIM_GRID_SIZE:SIM_GRID_SIZE * 2]]
            current_state_tuple = tuple(map(tuple, current_state_list))

        if current_state_tuple not in generated_states_tuples and current_state_tuple != SIM_STANDARD_GOAL_STATE_TUPLE:
            belief_set.append(current_state_list)
            generated_states_tuples.add(current_state_tuple)

    while len(belief_set) < num_states:
        fixed_top_row = copy.deepcopy(SIM_PARTIAL_OBSERVABLE_GOAL_FIXED_PART[0])
        remaining_numbers = [n for n in range(SIM_GRID_SIZE * SIM_GRID_SIZE) if n not in fixed_top_row]
        random.shuffle(remaining_numbers)
        state_m = [fixed_top_row,
                   remaining_numbers[0:SIM_GRID_SIZE],
                   remaining_numbers[SIM_GRID_SIZE:SIM_GRID_SIZE * 2]]
        state_t = tuple(map(tuple, state_m))
        if state_t not in generated_states_tuples:
            belief_set.append(state_m)
            generated_states_tuples.add(state_t)
        elif belief_set:
            belief_set.append(copy.deepcopy(belief_set[0]))
        else:
            s = copy.deepcopy(SIM_STANDARD_GOAL_STATE_LIST)
            r_nums = s[1] + s[2]
            random.shuffle(r_nums)
            s[1] = r_nums[:SIM_GRID_SIZE]
            s[2] = r_nums[SIM_GRID_SIZE:]
            belief_set.append(s)
            break
    return belief_set[:num_states]


def sim_check_consistent_with_goal_fixed_part_po(state_list):
    return state_list[0] == SIM_PARTIAL_OBSERVABLE_GOAL_FIXED_PART[0]


class EightPuzzleApp:
    def __init__(self):
        pygame.init()
        self.base_screen_width = 1200
        self.base_screen_height = 750
        self.screen_width = self.base_screen_width
        self.screen_height = self.base_screen_height

        self.is_showing_solution_window = False  # Cờ cho cửa sổ solution

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("8-Puzzle Solver")
        self.font = pygame.freetype.SysFont("arial", 24)
        self.large_font = pygame.freetype.SysFont("arial", 36, bold=True)
        self.small_font = pygame.freetype.SysFont("arial", 18)
        self.results_font = pygame.freetype.SysFont("arial", 16)

        self.sim_tile_font_po = pygame.font.Font(None, int(SIM_DISPLAY_TILE_SIZE_PO * 0.7))
        self.sim_tile_font_non_obs = pygame.font.Font(None, int(SIM_DISPLAY_TILE_SIZE_NON_OBS * 0.7))
        self.sim_tile_font_and_or = pygame.font.Font(None, int(SIM_DISPLAY_TILE_SIZE_AND_OR * 0.6))
        self.sim_info_font = pygame.font.Font(None, 22)
        self.sim_status_font = pygame.font.Font(None, 24)
        self.sim_button_font = pygame.font.Font(None, 26)

        self.clock = pygame.time.Clock()
        self.default_initial_state_list = [1, 2, 3, 4, 0, 5, 6, 7, 8]
        self.goal_state_1d = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.goal_state_2d = SIM_STANDARD_GOAL_STATE_LIST

        self.initial_state = self.default_initial_state_list.copy()
        self.current_state = self.initial_state.copy()

        self.algorithm = None
        self.solution_path = []
        self.current_step = 0
        self.is_running_animation = False
        self.solve_time = 0
        self.buttons = []
        self.selected_algo = None
        self.clicked_button_text = None
        self.click_time = 0
        self.running_action_text = None
        self.needs_reset = False

        self.complex_search_result_text = ""
        self.complex_actual_initial_state = None
        self.complex_use_default_setup = True

        self.root = Tk()
        self.root.withdraw()

        self.scroll_y_main = 0
        self.scrollable_content_height = 0
        self.visible_scrollable_area_height = 0
        self.scrollable_area_y_start = 350

        self.complex_results_scroll_y = 0
        self.complex_results_total_text_height = 0
        self.complex_results_panel_rect = pygame.Rect(0, 0, 0, 0)

        self.q_table = {}
        self.v_table = {}
        self.q_learning_trained = False
        self.is_q_learning_training_active = False
        self.action_map = {
            0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)
        }
        self.num_actions = len(self.action_map)
        self.app_should_quit = False

        self.active_simulation = None
        self.and_or_sim = None
        self.partially_obs_sim = None
        self.non_obs_sim = None

        self.setup_initial_state_board()
        self.setup_gui_buttons()

    def initialize_simulations_if_needed(self):
        if self.complex_results_panel_rect.width == 0:
            self._calculate_panel_rects()

        if not self.and_or_sim and self.complex_results_panel_rect.width > 0:
            self.and_or_sim = AndOrSearchSim(self, self.complex_results_panel_rect)
        if not self.partially_obs_sim and self.complex_results_panel_rect.width > 0:
            self.partially_obs_sim = PartiallyObservableSim(self, self.complex_results_panel_rect)
        if not self.non_obs_sim and self.complex_results_panel_rect.width > 0:
            self.non_obs_sim = NonObservableAutoRandomSim(self, self.complex_results_panel_rect)

    def _calculate_panel_rects(self):
        board_tile_size = min(self.screen_width // 15, self.screen_height // 8)
        board_tile_size = max(1, board_tile_size)  # Ngăn tile size bằng 0
        goal_board_x_start = 50 + board_tile_size * 3 + 30
        goal_board_width = board_tile_size * 3
        goal_board_end_x = goal_board_x_start + goal_board_width
        panel_margin_left = 25
        panel_x = goal_board_end_x + panel_margin_left
        panel_y = 50
        available_width_for_panel = self.screen_width - panel_x - 20
        panel_width = max(200, available_width_for_panel)
        panel_height = self.screen_height - panel_y - 20
        panel_height = max(200, panel_height)
        self.complex_results_panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

    @staticmethod
    def validate_single_state(state_list_2d):
        if not state_list_2d or len(state_list_2d) != 3: return False, "State must have 3 rows."
        flat_state = [num for row in state_list_2d for num in row]
        if len(flat_state) != 9: return False, "State must contain exactly 9 numbers."
        if not all(isinstance(num, int) and 0 <= num <= 8 for num in
                   flat_state): return False, "Numbers must be integers between 0 and 8."
        if sorted(flat_state) != list(
                range(9)): return False, "State must contain each number from 0 to 8 exactly once."
        return True, ""

    def get_single_state_from_user(self, prompt_message):
        while True:
            self.root.attributes('-topmost', True)
            state_str = simpledialog.askstring("Input State", prompt_message, parent=self.root)
            self.root.attributes('-topmost', False)
            if state_str is None: return None
            try:
                rows_str_list = state_str.split('/')
                if len(rows_str_list) != 3: raise ValueError("Input must contain 3 rows separated by '/'.")
                state_list_2d = [[int(n) for n in row_str_item.strip().split()] for row_str_item in rows_str_list]
                if any(len(row) != 3 for row in state_list_2d): raise ValueError(
                    "Each row must contain exactly 3 numbers.")
                is_valid, msg = self.validate_single_state(state_list_2d)
                if is_valid:
                    return state_list_2d
                else:
                    messagebox.showerror("Invalid State", msg, parent=self.root)
            except ValueError as e:
                messagebox.showerror("Invalid Format", f"Input error: {e}\nFormat: 'N N N / N N N / N N N'",
                                     parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Unexpected error: {e}", parent=self.root)

    def initialize_single_physical_state(self, for_complex_algo=False):
        self.root.attributes('-topmost', True)
        prompt_title = "Initialize Physical State"
        prompt_message = "Use default initial physical state?\n([1,2,3],[4,0,5],[6,7,8])"
        if for_complex_algo:
            prompt_title = "Define Initial Physical State (for Context)"
            prompt_message = "Define an initial physical state for context?\n(Default: [1,2,3],[4,0,5],[6,7,8])\nThis state is the 'actual' state if the environment were complex."
        use_default = messagebox.askyesno(prompt_title, prompt_message, parent=self.root)
        self.root.attributes('-topmost', False)
        if use_default:
            return [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
        else:
            return self.get_single_state_from_user("Input initial physical state:\nFormat 'N N N / N N N / N N N'")

    def setup_initial_state_board(self):
        state_2d = self.initialize_single_physical_state()
        if state_2d is None:
            self.initial_state = self.default_initial_state_list.copy()
        else:
            temp_flat_state = [num for row in state_2d for num in row]
            if self.is_solvable(temp_flat_state, self.goal_state_1d):
                self.initial_state = temp_flat_state
            else:
                messagebox.showerror("Invalid State",
                                     "The provided state for the main board is not solvable. Using default.",
                                     parent=self.root)
                self.initial_state = self.default_initial_state_list.copy()
        self.current_state = self.initial_state.copy()

    def setup_gui_buttons(self):
        button_height, button_spacing_y, group_label_height, group_spacing_y, current_y_relative = 40, 10, 30, 20, 0
        current_y_relative += group_label_height
        y_uninformed = current_y_relative
        self.buttons = [
            (pygame.Rect(50, y_uninformed, 100, button_height), "BFS", lambda: self.set_algorithm_standard("bfs"),
             "uninformed"),
            (pygame.Rect(160, y_uninformed, 100, button_height), "DFS", lambda: self.set_algorithm_standard("dfs"),
             "uninformed"),
            (pygame.Rect(270, y_uninformed, 100, button_height), "UCS", lambda: self.set_algorithm_standard("ucs"),
             "uninformed"),
            (pygame.Rect(380, y_uninformed, 100, button_height), "IDS", lambda: self.set_algorithm_standard("ids"),
             "uninformed"),
        ]
        current_y_relative += button_height + group_spacing_y
        current_y_relative += group_label_height
        y_informed = current_y_relative
        self.buttons.extend([
            (pygame.Rect(50, y_informed, 100, button_height), "Greedy", lambda: self.set_algorithm_standard("greedy"),
             "informed"),
            (pygame.Rect(160, y_informed, 100, button_height), "A*", lambda: self.set_algorithm_standard("astar"),
             "informed"),
            (pygame.Rect(270, y_informed, 100, button_height), "IDA*", lambda: self.set_algorithm_standard("ida"),
             "informed"),
        ])
        current_y_relative += button_height + group_spacing_y
        current_y_relative += group_label_height
        y_local_1 = current_y_relative
        self.buttons.extend([
            (
                pygame.Rect(50, y_local_1, 100, button_height), "SimpleHC",
                lambda: self.set_algorithm_standard("simplehc"),
                "local"),
            (pygame.Rect(160, y_local_1, 100, button_height), "SteepestHC",
             lambda: self.set_algorithm_standard("steepesthc"), "local"),
            (pygame.Rect(270, y_local_1, 100, button_height), "StochasticHC",
             lambda: self.set_algorithm_standard("stochastichc"), "local"),
            (pygame.Rect(380, y_local_1, 100, button_height), "SimAnneal",
             lambda: self.set_algorithm_standard("simanneal"), "local"),
        ])
        current_y_relative += button_height + button_spacing_y
        y_local_2 = current_y_relative
        self.buttons.extend([
            (pygame.Rect(50, y_local_2, 100, button_height), "Genetic", lambda: self.set_algorithm_standard("genetic"),
             "local"),
            (pygame.Rect(160, y_local_2, 100, button_height), "Beam", lambda: self.set_algorithm_standard("beam"),
             "local"),
        ])
        current_y_relative += button_height + group_spacing_y
        current_y_relative += group_label_height
        y_complex = current_y_relative
        self.buttons.extend([
            (pygame.Rect(50, y_complex, 100, button_height), "AND-OR", lambda: self.set_algorithm_complex("and_or_sim"),
             "complex"),
            (pygame.Rect(160, y_complex, 110, button_height), "Sensorless",
             lambda: self.set_algorithm_complex("non_obs_sim"), "complex"),
            (pygame.Rect(280, y_complex, 120, button_height), "PartiallyObs",
             lambda: self.set_algorithm_complex("partially_obs_sim"), "complex"),
        ])
        current_y_relative += button_height + group_spacing_y
        current_y_relative += group_label_height

        y_constrained_path = current_y_relative
        self.buttons.extend([
            (pygame.Rect(50, y_constrained_path, 250, button_height), "Backtracking (2-5 Adj)",
             lambda: self.set_algorithm_constrained_path("bp_25adj"), "constrained_path"),
            (pygame.Rect(310, y_constrained_path, 300, button_height), "ForwardChecking (2-5 Adj)",
             lambda: self.set_algorithm_constrained_path("fc_25adj"), "constrained_path"),
            (pygame.Rect(50, y_constrained_path + button_height + button_spacing_y, 300, button_height),
             "MinConflicts Repair (2-5 Adj)", lambda: self.set_algorithm_constrained_path("mc_25adj_repair"),
             "constrained_path_repair"),
        ])
        current_y_relative += (button_height * 2) + button_spacing_y + group_spacing_y
        current_y_relative += group_label_height

        y_rl = current_y_relative
        self.buttons.extend([
            (pygame.Rect(50, y_rl, 220, button_height), "Q-Learning (Train & Solve)",
             lambda: self.set_algorithm_rl("rl_q_learning_train_solve"), "rl"),
            (pygame.Rect(280, y_rl, 230, button_height), "TD Learning (Train & Solve)",
             lambda: self.set_algorithm_rl("rl_td_learning_train_solve"), "rl"),
        ])
        current_y_relative += button_height + group_spacing_y
        y_actions = current_y_relative
        self.buttons.extend([
            (pygame.Rect(50, y_actions, 100, button_height), "Run", self.run_selected_algorithm, "action"),
            (pygame.Rect(160, y_actions, 100, button_height), "Solution",
             lambda: asyncio.create_task(self.show_solution_path_standard()), "action"),
            (pygame.Rect(270, y_actions, 100, button_height), "Reset", self.reset_all, "action"),
        ])
        current_y_relative += button_height + group_spacing_y
        self.scrollable_content_height = current_y_relative

    def set_algorithm_standard(self, algo_key):
        if self.is_q_learning_training_active or self.active_simulation: return
        if self.needs_reset: messagebox.showwarning("Warning", "Please press Reset before selecting another algorithm!",
                                                    parent=self.root); return
        self.selected_algo = algo_key
        self.algorithm = algo_key
        self.complex_search_result_text = ""
        self.complex_results_scroll_y = 0
        self.active_simulation = None
        self.draw()

    def set_algorithm_complex(self, algo_key):
        if self.is_q_learning_training_active or (self.active_simulation and self.algorithm == algo_key): return
        if self.needs_reset and not self.active_simulation: messagebox.showwarning("Warning",
                                                                                   "Please press Reset before selecting another algorithm!",
                                                                                   parent=self.root); return

        self.initialize_simulations_if_needed()

        self.selected_algo = algo_key
        self.algorithm = algo_key
        self.solution_path = []
        self.complex_search_result_text = ""
        self.complex_results_scroll_y = 0
        self.needs_reset = False

        if algo_key == "and_or_sim":
            self.active_simulation = self.and_or_sim
            if self.and_or_sim: self.and_or_sim.reset_simulation()
        elif algo_key == "partially_obs_sim":
            self.active_simulation = self.partially_obs_sim
            if self.partially_obs_sim: self.partially_obs_sim.reset_simulation_full()
        elif algo_key == "non_obs_sim":
            self.active_simulation = self.non_obs_sim
            if self.non_obs_sim: self.non_obs_sim.reset_simulation()
        else:
            self.active_simulation = None
        self.draw()

    def set_algorithm_constrained_path(self, algo_key):
        if self.is_q_learning_training_active or self.active_simulation: return
        if self.needs_reset:
            messagebox.showwarning("Warning", "Please press Reset before selecting another algorithm!",
                                   parent=self.root)
            return
        self.selected_algo = algo_key
        self.algorithm = algo_key
        self.complex_search_result_text = ""
        self.complex_results_scroll_y = 0
        self.active_simulation = None
        self.solution_path = []
        self.current_step = 0
        self.draw()

    def set_algorithm_rl(self, algo_key):
        if self.is_q_learning_training_active or self.active_simulation: return
        if self.needs_reset: messagebox.showwarning("Warning",
                                                    "Please press Reset before selecting another algorithm/simulation!",
                                                    parent=self.root); return
        self.selected_algo = algo_key
        self.algorithm = algo_key
        self.solution_path = []
        self.complex_search_result_text = ""
        self.complex_results_scroll_y = 0
        self.active_simulation = None
        self.draw()

    def prompt_complex_init_options(self, algo_name_display_key):
        self.root.attributes('-topmost', True)
        choice = messagebox.askyesnocancel(f"Initialize {algo_name_display_key.replace('_', ' ').title()}",
                                           f"Use default setup for {algo_name_display_key.replace('_', ' ').title()}?\n\n(Yes for Default, No to define an initial physical state for context)",
                                           parent=self.root)
        self.root.attributes('-topmost', False)
        if choice is None: self.selected_algo = None; self.algorithm = None; self.complex_actual_initial_state = None; return
        self.complex_use_default_setup = choice
        if not self.complex_use_default_setup:
            state_2d = self.initialize_single_physical_state(for_complex_algo=True)
            if state_2d:
                temp_flat_state = [num for row in state_2d for num in row]
                if self.is_solvable(temp_flat_state, self.goal_state_1d):
                    self.complex_actual_initial_state = temp_flat_state
                else:
                    messagebox.showerror("Invalid State",
                                         "The provided physical state is not solvable. Using default context.",
                                         parent=self.root);
                    self.complex_actual_initial_state = self.default_initial_state_list.copy()
            else:
                self.selected_algo = None;
                self.algorithm = None;
                self.complex_actual_initial_state = None;
                return
        else:
            self.complex_actual_initial_state = self.default_initial_state_list.copy()

    def draw_board(self, surface, state_1d, x_pos, y_pos, label_text, tile_size=60):
        self.font.render_to(surface, (x_pos, y_pos - 30), label_text, (255, 255, 255))
        for i in range(3):
            for j in range(3):
                value = state_1d[i * 3 + j]
                tile_rect = pygame.Rect(x_pos + j * tile_size, y_pos + i * tile_size, tile_size, tile_size)
                pygame.draw.rect(surface, (100, 100, 100), tile_rect)
                if value != 0:
                    pygame.draw.rect(surface, (200, 200, 200), tile_rect.inflate(-4, -4))
                    text_surface, text_rect = self.font.render(str(value), (0, 0, 0))
                    surface.blit(text_surface, (tile_rect.x + (tile_size - text_rect.width) // 2,
                                                tile_rect.y + (tile_size - text_rect.height) // 2))
                else:
                    pygame.draw.rect(surface, (80, 80, 80), tile_rect.inflate(-4, -4))

    def draw_complex_results_panel(self):
        if self.complex_results_panel_rect.width == 0:
            self._calculate_panel_rects()

        pygame.draw.rect(self.screen, (40, 40, 40), self.complex_results_panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), self.complex_results_panel_rect, 2)
        title_y_offset = 10
        panel_title = "Algorithm Results/Explanation:"
        if self.algorithm:
            if "constrained_path" in self.algorithm or "bp_25adj" in self.algorithm or "fc_25adj" in self.algorithm or "mc_25adj_repair" in self.algorithm:
                panel_title = "Constrained Pathfinding Results:"
            elif "rl_" in self.algorithm:
                panel_title = "RL Simulation/Training Summary:"
            elif self.algorithm in ["and_or", "sensorless", "partially_observable"] and not self.active_simulation:
                panel_title = "Complex Search Results (Text):"

        self.font.render_to(self.screen, (
            self.complex_results_panel_rect.x + 10, self.complex_results_panel_rect.y + title_y_offset), panel_title,
                            (220, 220, 220))
        text_render_start_y_abs = self.complex_results_panel_rect.y + title_y_offset + self.font.get_sized_height() + 10
        text_area_height = self.complex_results_panel_rect.height - (
                text_render_start_y_abs - self.complex_results_panel_rect.y) - 10
        if text_area_height <= 0: return

        text_surface_rect = pygame.Rect(self.complex_results_panel_rect.x + 15, text_render_start_y_abs,
                                        self.complex_results_panel_rect.width - 30, text_area_height)
        if text_surface_rect.width <= 0 or text_surface_rect.height <= 0: return

        text_surface = self.screen.subsurface(text_surface_rect)
        text_surface.fill((40, 40, 40))
        current_render_y_on_subsurface = self.complex_results_scroll_y
        self.complex_results_total_text_height = 0
        if self.complex_search_result_text:
            lines = self.complex_search_result_text.split('\n')
            line_height_with_spacing = self.results_font.get_sized_height() + 3
            for line_text in lines:
                self.results_font.render_to(text_surface, (0, current_render_y_on_subsurface), line_text,
                                            (200, 200, 200))
                current_render_y_on_subsurface += line_height_with_spacing
                self.complex_results_total_text_height += line_height_with_spacing

    def draw_training_overlay(self):
        overlay_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 180))
        self.screen.blit(overlay_surface, (0, 0))
        text_surf, text_rect = self.large_font.render("RL Training in Progress... Please Wait", (255, 255, 0))
        text_rect.center = (self.screen_width // 2, self.screen_height // 2)
        self.screen.blit(text_surf, text_rect)

    def draw(self):
        self.screen.fill((50, 50, 50))
        # Đảm bảo self.screen_width và self.screen_height phản ánh kích thước thực tế hiện tại của màn hình
        actual_width, actual_height = self.screen.get_size()
        if self.screen_width != actual_width or self.screen_height != actual_height:
            self.screen_width = actual_width
            self.screen_height = actual_height

        current_screen_width, current_screen_height = self.screen_width, self.screen_height  # Sử dụng các giá trị đã được đồng bộ hóa

        self.visible_scrollable_area_height = current_screen_height - self.scrollable_area_y_start - 20
        board_tile_size = min(current_screen_width // 15, current_screen_height // 8)
        board_tile_size = max(1, board_tile_size)  # Ngăn board_tile_size bằng 0 nếu cửa sổ quá nhỏ

        display_state_label = "Initial State"
        display_state_list = self.current_state
        is_animatable_algo = self.algorithm and "constrained_path" not in self.algorithm and "bp_25adj" not in self.algorithm and "fc_25adj" not in self.algorithm and "mc_25adj_repair" not in self.algorithm and self.algorithm not in [
            "and_or_sim", "non_obs_sim", "partially_obs_sim"] and "rl_" not in self.algorithm

        is_constrained_path_algo = self.algorithm and (
                "constrained_path" in self.algorithm or "bp_25adj" in self.algorithm or "fc_25adj" in self.algorithm or "mc_25adj_repair" in self.algorithm)
        is_rl_algo_running_animation = self.algorithm and "rl_" in self.algorithm and self.is_running_animation

        if self.algorithm in ["and_or", "sensorless", "partially_observable"] and not self.active_simulation:
            if self.complex_actual_initial_state:
                display_state_label = "Actual Initial (Context)"
                display_state_list = self.complex_actual_initial_state
        elif is_animatable_algo or is_constrained_path_algo or is_rl_algo_running_animation:
            if self.is_running_animation:
                display_state_label = "Current State"
                display_state_list = self.current_state  # Cập nhật để hiển thị trạng thái hiện tại của animation
            elif self.solution_path and self.current_step == len(self.solution_path) and len(self.solution_path) > 0:
                display_state_label = "Final State (Goal)" if self.current_state == self.goal_state_1d else "Final State (Simulated)"
                display_state_list = self.current_state

        self.draw_board(self.screen, display_state_list, 50, 50, display_state_label, board_tile_size)
        self.draw_board(self.screen, self.goal_state_1d, 50 + board_tile_size * 3 + 30, 50, "Goal State",
                        board_tile_size)

        self._calculate_panel_rects()  # Sẽ sử dụng self.screen_width/height đã được cập nhật

        if self.active_simulation:
            self.active_simulation.content_rect = self.complex_results_panel_rect
            self.active_simulation.draw(self.screen, pygame.mouse.get_pos())
        else:
            self.draw_complex_results_panel()

        group_label_y_offset = -25

        def draw_group_label_if_visible(group_name_filter, label_text):
            first_button = next((btn for btn in self.buttons if btn[3] == group_name_filter), None)
            if first_button:
                label_y = self.scrollable_area_y_start + first_button[0].y + self.scroll_y_main + group_label_y_offset
                if self.scrollable_area_y_start - abs(
                        group_label_y_offset) - 5 < label_y < current_screen_height:  # Sử dụng current_screen_height đã đồng bộ
                    self.small_font.render_to(self.screen, (50, label_y), label_text, (255, 255, 255))

        draw_group_label_if_visible("uninformed", "Uninformed Search:")
        draw_group_label_if_visible("informed", "Informed Search:")
        draw_group_label_if_visible("local", "Local Search:")
        draw_group_label_if_visible("complex", "Complex Environment Search:")
        draw_group_label_if_visible("constrained_path", "Constrained Pathfinding (2-5 Adj):")
        draw_group_label_if_visible("rl", "Reinforcement Learning (Train & Solve):")

        button_text_to_algo_key_map = {
            "BFS": "bfs", "DFS": "dfs", "UCS": "ucs", "IDS": "ids", "Greedy": "greedy", "A*": "astar", "IDA*": "ida",
            "SimpleHC": "simplehc", "SteepestHC": "steepesthc", "StochasticHC": "stochastichc",
            "SimAnneal": "simanneal",
            "Genetic": "genetic", "Beam": "beam", "AND-OR": "and_or_sim", "Sensorless": "non_obs_sim",
            "PartiallyObs": "partially_obs_sim",
            "Backtracking (2-5 Adj)": "bp_25adj",
            "ForwardChecking (2-5 Adj)": "fc_25adj",
            "MinConflicts Repair (2-5 Adj)": "mc_25adj_repair",
            "Q-Learning (Train & Solve)": "rl_q_learning_train_solve",
            "TD Learning (Train & Solve)": "rl_td_learning_train_solve"
        }
        for original_rect, button_text, _, _group in self.buttons:
            scrolled_rect = pygame.Rect(original_rect.x,
                                        self.scrollable_area_y_start + original_rect.y + self.scroll_y_main,
                                        original_rect.width, original_rect.height)
            if scrolled_rect.bottom > self.scrollable_area_y_start and scrolled_rect.top < current_screen_height:  # Sử dụng current_screen_height đã đồng bộ
                button_color = (150, 150, 150)
                algo_key_for_check = button_text_to_algo_key_map.get(button_text)
                if self.selected_algo == algo_key_for_check: button_color = (0, 200, 0)
                if self.running_action_text == button_text:
                    button_color = (255, 165, 0)
                elif self.clicked_button_text == button_text and (time.time() - self.click_time) < 0.2:
                    button_color = (200, 200, 0)
                pygame.draw.rect(self.screen, button_color, scrolled_rect)
                text_surf_btn, text_rect_btn = self.small_font.render(button_text, (0, 0, 0))
                self.screen.blit(text_surf_btn, (scrolled_rect.x + (scrolled_rect.width - text_rect_btn.width) // 2,
                                                 scrolled_rect.y + (scrolled_rect.height - text_rect_btn.height) // 2))

        info_text_x = 50
        info_text_y = current_screen_height - 70  # Gần cuối màn hình

        if self.scrollable_area_y_start < current_screen_height - 70:  # Nếu có không gian dưới các nút
            info_text_y = self.scrollable_area_y_start + self.scrollable_content_height + self.scroll_y_main + 10
            if info_text_y > current_screen_height - 30: info_text_y = current_screen_height - 70  # Giới hạn lại

        if not self.active_simulation and self.complex_results_panel_rect.width > 0:
            if self.complex_results_panel_rect.left > info_text_x + 200:  # Đủ chỗ bên trái panel
                info_text_y = self.complex_results_panel_rect.top
            else:  # Đặt bên dưới board chính
                info_text_x = 50
                info_text_y = 50 + board_tile_size * 3 + 30 + 30  # Dưới goal board
        elif self.active_simulation:
            info_text_x = 50
            info_text_y = current_screen_height - 70

        self.small_font.render_to(self.screen, (info_text_x+1300, info_text_y+650),
                                  f"Steps: {self.current_step if self.solution_path else 0}", (255, 255, 255))
        self.small_font.render_to(self.screen, (info_text_x+1300, info_text_y + 30+650), f"Time: {self.solve_time:.8f}s",
                                  (255, 255, 255))
        if self.is_q_learning_training_active: self.draw_training_overlay()
        pygame.display.flip()

    def _get_or_initialize_v_value(self, state_tuple):
        if state_tuple not in self.v_table:
            self.v_table[state_tuple] = 0.0
        return self.v_table[state_tuple]

    def run_td_value_prediction(self, episodes=7000, alpha=0.1, gamma=0.9, steps_per_episode=150, epsilon_td_start=0.5,
                                epsilon_td_decay=0.9995, epsilon_td_min=0.05):
        self.v_table = {}
        log = ["Starting TD Value Prediction (V(s) learning)..."]
        self.complex_search_result_text = "\n".join(log)
        self.draw()
        pygame.display.flip()
        goal_tuple = self._state_to_tuple(self.goal_state_1d)
        epsilon_td = epsilon_td_start

        for ep in range(episodes):
            if self.app_should_quit: break
            current_s_list = self.initial_state[:]

            for _step in range(steps_per_episode):
                if self.app_should_quit: break
                current_s_tuple = self._state_to_tuple(current_s_list)
                v_s = self._get_or_initialize_v_value(current_s_tuple)

                valid_moves = self.get_neighbors(current_s_list)
                if not valid_moves: break

                next_s_list = None
                if random.random() < epsilon_td:
                    next_s_list = random.choice(valid_moves)
                else:
                    best_v_next = -float('inf')
                    best_moves = []
                    for move in valid_moves:
                        move_tuple = self._state_to_tuple(move)
                        v_move = self._get_or_initialize_v_value(move_tuple)
                        if v_move > best_v_next:
                            best_v_next = v_move
                            best_moves = [move]
                        elif v_move == best_v_next:
                            best_moves.append(move)
                    if best_moves:
                        next_s_list = random.choice(best_moves)
                    else:  # Should not happen if valid_moves is not empty
                        next_s_list = random.choice(valid_moves)

                next_s_tuple = self._state_to_tuple(next_s_list)

                reward = 0.0
                if next_s_tuple == goal_tuple:
                    reward = 1.0
                else:
                    reward = -0.01

                v_s_next = self._get_or_initialize_v_value(next_s_tuple)

                td_target = reward
                if next_s_tuple != goal_tuple:
                    td_target += gamma * v_s_next

                td_error = td_target - v_s
                self.v_table[current_s_tuple] = v_s + alpha * td_error

                current_s_list = next_s_list
                if current_s_tuple == goal_tuple:
                    break

            epsilon_td = max(epsilon_td_min, epsilon_td * epsilon_td_decay)

            if (ep + 1) % (episodes // 100 if episodes >= 100 else 1) == 0 or ep == episodes - 1:
                v_start = self._get_or_initialize_v_value(self._state_to_tuple(self.initial_state))
                log_msg = f"TD Ep {ep + 1}/{episodes}, Eps_td: {epsilon_td:.3f}, V_table: {len(self.v_table)}, V(start): {v_start:.3f}"
                log.append(log_msg)
                print(log_msg)
                self.complex_search_result_text = "TD Value Prediction in Progress...\n" + "\n".join(log[-5:])
                self.draw()
                pygame.display.flip()
                for event_check in pygame.event.get():
                    if event_check.type == pygame.QUIT:
                        self.app_should_quit = True
                        break
                if self.app_should_quit: break

        if not self.app_should_quit:
            log.append(f"TD Value Prediction finished. {len(self.v_table)} states in V-table.")
        else:
            log.append("TD Value Prediction interrupted.")
        self.complex_search_result_text = "\n".join(log)
        self.draw()
        pygame.display.flip()

    def generate_path_from_v_values(self, start_state_list, max_steps=100):
        if not self.v_table:
            self.complex_search_result_text += "\nError: V-table is empty. Cannot generate path."
            return []

        current_s_list = start_state_list[:]
        path = [current_s_list[:]]
        goal_tuple = self._state_to_tuple(self.goal_state_1d)
        log_path_gen = ["Generating path from V-values:"]

        for step_count_path in range(max_steps):
            if self.app_should_quit: break
            current_s_tuple = self._state_to_tuple(current_s_list)
            if current_s_tuple == goal_tuple:
                log_path_gen.append(f"Goal reached in {step_count_path} steps.")
                break

            valid_moves = self.get_neighbors(current_s_list)
            if not valid_moves:
                log_path_gen.append("Path generation stuck: No valid moves.")
                break

            best_next_s_list = None
            max_v_next = -float('inf')

            potential_best_next_states = []
            for move_s_list in valid_moves:
                move_s_tuple = self._state_to_tuple(move_s_list)
                v_val = self._get_or_initialize_v_value(move_s_tuple)
                if v_val > max_v_next:
                    max_v_next = v_val
                    potential_best_next_states = [move_s_list]
                elif v_val == max_v_next:
                    potential_best_next_states.append(move_s_list)

            if potential_best_next_states:
                best_next_s_list = random.choice(potential_best_next_states)
            else:
                log_path_gen.append(
                    "Path generation stuck: Could not determine best next state (all V-values might be low or unvisited). Choosing random from valid moves.")
                best_next_s_list = random.choice(valid_moves)

            current_s_list = best_next_s_list
            path.append(current_s_list[:])

            if len(path) > 10:
                sub_path_tuples_check = [tuple(s_check) for s_check in path[-5:]]
                for i_check in range(len(path) - 5):
                    if tuple(path[i_check]) in sub_path_tuples_check and tuple(
                            path[i_check + 1]) in sub_path_tuples_check:
                        log_path_gen.append("Path generation might be stuck in a loop (detected).")
                        self.app_should_quit = True
                        break
            if self.app_should_quit: break
        else:
            if current_s_tuple != goal_tuple:
                log_path_gen.append(f"Goal not reached in {max_steps} steps. Path length: {len(path) - 1}.")

        self.complex_search_result_text += "\n" + "\n".join(log_path_gen)
        return path

    def _state_to_tuple(self, state_list):
        return tuple(state_list)

    def _get_or_initialize_q_values(self, state_tuple):
        if state_tuple not in self.q_table: self.q_table[state_tuple] = [0.0] * self.num_actions
        return self.q_table[state_tuple]

    def _get_valid_actions_with_next_states(self, state_list):
        valid_actions_info = []
        zero_idx = state_list.index(0) if 0 in state_list else -1
        if zero_idx == -1: return []
        r, c = zero_idx // 3, zero_idx % 3
        for act_idx, (dr, dc) in self.action_map.items():
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_state = state_list[:]
                tile_to_move = nr * 3 + nc
                new_state[zero_idx], new_state[tile_to_move] = new_state[tile_to_move], new_state[zero_idx]
                valid_actions_info.append((act_idx, new_state))
        return valid_actions_info

    def train_q_learning_agent(self, episodes=10000, alpha=0.1, gamma=0.9, eps_start=1.0, eps_decay=0.999, eps_min=0.01,
                               steps_per_episode=100):
        self.is_q_learning_training_active = True
        epsilon = eps_start
        log = []
        self.q_table = {}
        self.q_learning_trained = False
        goal_tuple = self._state_to_tuple(self.goal_state_1d)
        initial_template = self.initial_state[:]
        self.complex_search_result_text = "Starting Q-Learning Training...\n"
        self.draw()
        pygame.display.flip()

        for ep in range(episodes):
            if self.app_should_quit: break
            current_s_list = initial_template[:]
            current_s_tuple = self._state_to_tuple(current_s_list)
            ep_reward = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.app_should_quit = True; break
            if self.app_should_quit: break
            for _step in range(steps_per_episode):
                if self.app_should_quit: break
                q_curr = self._get_or_initialize_q_values(current_s_tuple)
                valid_acts = self._get_valid_actions_with_next_states(current_s_list)
                if not valid_acts: break
                act_idx_to_take = random.choice(valid_acts)[0] if random.random() < epsilon else \
                    max(valid_acts, key=lambda item: q_curr[item[0]])[0]
                next_s_list = next(s for idx, s in valid_acts if idx == act_idx_to_take)
                next_s_tuple = self._state_to_tuple(next_s_list)
                reward = 20.0 if next_s_tuple == goal_tuple else -0.1
                ep_reward += reward
                q_next = self._get_or_initialize_q_values(next_s_tuple)
                max_q_next = max(q_next[info[0]] for info in self._get_valid_actions_with_next_states(
                    next_s_list)) if next_s_tuple != goal_tuple and self._get_valid_actions_with_next_states(
                    next_s_list) else 0.0
                target_q = reward + gamma * max_q_next if next_s_tuple != goal_tuple else reward
                q_curr[act_idx_to_take] += alpha * (target_q - q_curr[act_idx_to_take])
                current_s_list, current_s_tuple = next_s_list, next_s_tuple
                if current_s_tuple == goal_tuple: break
            epsilon = max(eps_min, epsilon * eps_decay)
            if (ep + 1) % 200 == 0 or ep == episodes - 1:
                log_msg = f"Episode {ep + 1}/{episodes}, Eps: {epsilon:.3f}, Reward: {ep_reward:.1f}"
                log.append(log_msg)
                print(log_msg)
                self.complex_search_result_text = "Q-Learning Training in Progress...\n" + "\n".join(log[-5:])
                self.draw()
                pygame.display.flip()

        if not self.app_should_quit:
            self.q_learning_trained = True
            final_msg = f"Q-Learning Training Complete. Total Episodes: {episodes}.\nFinal Epsilon: {epsilon:.4f}"
            log.append(final_msg)
            self.complex_search_result_text = "\n".join(log[-10:])
            print(final_msg)
        else:
            self.complex_search_result_text += "\nQ-Learning Training Interrupted."
            print("Q-Learning Training Interrupted.")
        self.is_q_learning_training_active = False
        self.draw()
        pygame.display.flip()

    def solve_puzzle_with_q_policy(self, start_state_list, max_steps=100):
        if not self.q_learning_trained:
            self.complex_search_result_text += "\nQ-Learning model not trained. Please train first."
            return []
        current_s_list = start_state_list[:]
        path = [current_s_list[:]]
        goal_tuple = self._state_to_tuple(self.goal_state_1d)
        log_exec = ["Executing Q-policy:"]
        for step_count in range(max_steps):
            if self.app_should_quit: return path
            current_s_tuple = self._state_to_tuple(current_s_list)
            if current_s_tuple == goal_tuple:
                log_exec.append(f"Goal reached in {step_count} steps.")
                break
            q_curr = self._get_or_initialize_q_values(current_s_tuple)
            valid_acts = self._get_valid_actions_with_next_states(current_s_list)
            if not valid_acts:
                log_exec.append("Stuck: No valid actions.")
                break
            best_act_indices = [item[0] for item in valid_acts if
                                q_curr[item[0]] == max(q_curr[v_act[0]] for v_act in valid_acts)]
            if not best_act_indices:
                log_exec.append(f"Stuck: No best action. Q-values: {q_curr}")
                break
            chosen_act_idx = random.choice(best_act_indices)
            next_s_list = next(s for idx, s in valid_acts if idx == chosen_act_idx)
            if next_s_list is None:
                log_exec.append("Error: Could not find next state.")
                break
            current_s_list = next_s_list
            path.append(current_s_list[:])
            if len(path) > 15 and path[-1] in path[:-10]:
                log_exec.append("Policy might be stuck in a loop.")
                break
        else:  # For loop finished without break (goal not reached)
            log_exec.append(f"Goal not reached in {max_steps} steps. Path length: {len(path) - 1}.")
        self.complex_search_result_text += "\n" + "\n".join(log_exec)
        return path

    def run_selected_algorithm(self):
        if self.is_q_learning_training_active: return
        if self.needs_reset and not self.active_simulation:
            messagebox.showwarning("Warning", "Please press Reset before running again!", parent=self.root)
            return
        if not self.algorithm:
            messagebox.showwarning("Warning", "Please select an algorithm first!", parent=self.root)
            return
        if self.is_running_animation and self.algorithm != "rl_q_learning_train_solve" and self.algorithm != "rl_td_learning_train_solve":
            messagebox.showinfo("Information", "Animation is running, please wait or Reset.", parent=self.root)
            return

        self.running_action_text = "Run"
        self.draw()
        pygame.time.wait(100)
        self.current_step = 0
        self.solve_time = 0
        start_time = time.time()
        self.complex_search_result_text = ""
        self.solution_path = []
        self.app_should_quit = False
        current_initial = self.initial_state[:]
        goal_target = self.goal_state_1d[:]

        if self.algorithm in ["and_or_sim", "non_obs_sim", "partially_obs_sim"]:
            self.is_running_animation = False
            self.complex_results_scroll_y = 0
            self.initialize_simulations_if_needed()
            if self.algorithm == "and_or_sim" and self.and_or_sim:
                self.active_simulation = self.and_or_sim
                self.and_or_sim.reset_simulation()
            elif self.algorithm == "non_obs_sim" and self.non_obs_sim:
                self.active_simulation = self.non_obs_sim
                self.non_obs_sim.reset_simulation()
            elif self.algorithm == "partially_obs_sim" and self.partially_obs_sim:
                self.active_simulation = self.partially_obs_sim
                self.partially_obs_sim.reset_simulation_full()
            self.needs_reset = True
        elif self.algorithm in ["and_or", "sensorless", "partially_observable"]:
            self.is_running_animation = False
            self.complex_results_scroll_y = 0
            initial_context = self.complex_actual_initial_state if self.complex_actual_initial_state else self.default_initial_state_list
            if self.algorithm == "and_or": self.complex_search_result_text = self.generate_and_or_plan_text(
                initial_context)
            self.needs_reset = True

        elif self.algorithm in ["bp_25adj", "fc_25adj"]:
            self.is_running_animation = True
            if not self.check_2_5_adjacency(current_initial):
                self.complex_search_result_text = "Error: Initial state of the main board violates 2 & 5 adjacency constraint.\nPlease Reset and select a valid initial state."
                messagebox.showerror("Constraint Violated", self.complex_search_result_text, parent=self.root)
                self.is_running_animation = False
                self.solution_path = []
            elif not self.check_2_5_adjacency(goal_target):
                self.complex_search_result_text = "Error: Goal state violates 2 & 5 adjacency constraint."
                messagebox.showerror("Constraint Violated", self.complex_search_result_text, parent=self.root)
                self.is_running_animation = False
                self.solution_path = []
            else:
                if self.algorithm == "bp_25adj":
                    self.complex_search_result_text = "Running Backtracking (2-5 Adjacency)...\n"
                    self.solution_path = self.backtracking_8puzzle_constrained(current_initial, goal_target)
                elif self.algorithm == "fc_25adj":
                    self.complex_search_result_text = "Running Forward Checking (2-5 Adjacency)...\n"
                    self.solution_path = self.forward_checking_8puzzle_constrained(current_initial, goal_target)

                if self.solution_path:
                    self.complex_search_result_text += f"Solution found with {len(self.solution_path) - 1} moves."
                    if self.solution_path[-1] != goal_target:
                        self.complex_search_result_text += "\nWarning: Final state in path is not the goal."
                elif not self.app_should_quit:
                    self.complex_search_result_text += "No solution found satisfying the constraints."
                    if not self.is_running_animation:  # Avoid showing messagebox if animation was intended
                        messagebox.showerror("No Solution", self.complex_search_result_text)
                    self.is_running_animation = False
            self.needs_reset = True

        elif self.algorithm == "mc_25adj_repair":
            self.is_running_animation = True
            self.complex_search_result_text = "Attempting to generate initial path with A* (standard)...\n"
            self.draw()
            pygame.display.flip()

            astar_path = self.astar(current_initial, goal_target)

            if not astar_path:
                self.complex_search_result_text += "A* (standard) could not find an initial path to the goal.\nMinConflicts cannot proceed."
                messagebox.showwarning("MinConflicts", self.complex_search_result_text, parent=self.root)
                self.is_running_animation = False
            elif not self.check_2_5_adjacency(astar_path[0]) or not self.check_2_5_adjacency(astar_path[-1]):
                self.complex_search_result_text += "MinConflicts: Start or End of A* path violates 2-5 adjacency. Cannot repair."
                messagebox.showerror("MinConflicts Error", self.complex_search_result_text, parent=self.root)
                self.is_running_animation = False
            else:
                self.complex_search_result_text += f"A* (standard) found an initial path of length {len(astar_path) - 1}.\nRunning MinConflicts Repair (2-5 Adjacency) on this path...\n"
                self.draw()
                pygame.display.flip()

                path_to_repair = [list(state) for state in astar_path]
                repaired_path = self.min_conflicts_8puzzle_repair_constrained(path_to_repair)

                if repaired_path:
                    self.solution_path = repaired_path
                    self.complex_search_result_text += f"\nMinConflicts process completed. Path length after repair: {len(repaired_path) - 1}"

                    final_conflicts = self._count_conflicts_for_mc_report(repaired_path)
                    self.complex_search_result_text += f"\nFinal conflicts in repaired path: {final_conflicts}"
                    if final_conflicts == 0 and repaired_path[-1] == self.goal_state_1d:
                        self.complex_search_result_text += "\nPath successfully repaired and leads to goal."
                    else:
                        self.complex_search_result_text += "\nPath repair might be incomplete or path does not lead to goal, or goal not reached."
                        if repaired_path[-1] != self.goal_state_1d:
                            self.complex_search_result_text += f"\nWarning: Repaired path ends at {self.format_state_for_display(repaired_path[-1])} instead of goal."
                            self.is_running_animation = False
                else:
                    self.complex_search_result_text += "MinConflicts: Repair process failed to return a path."
                    self.is_running_animation = False
            self.needs_reset = True

        elif self.algorithm == "rl_q_learning_train_solve":
            self.is_running_animation = False
            self.complex_results_scroll_y = 0
            self.train_q_learning_agent()
            self.current_state = self.initial_state[:]  # Reset current state before solving
            self.draw()  # Update display after training
            if self.q_learning_trained and not self.app_should_quit:
                self.current_state = self.initial_state[:]  # Ensure starting from initial for policy execution
                self.solution_path = self.solve_puzzle_with_q_policy(self.initial_state[:])
                if self.solution_path and self.solution_path[-1] == self.goal_state_1d:
                    self.is_running_animation = True
                    self.current_state = self.solution_path[0]  # Start animation from first step
                else:
                    self.is_running_animation = False
                    self.complex_search_result_text += "\nQ-policy did not reach goal or no path." if not self.solution_path or \
                                                                                                      self.solution_path[
                                                                                                          -1] != self.goal_state_1d else ""
            else:
                self.solution_path = []
                self.is_running_animation = False
            self.needs_reset = True
            self.draw()
        elif self.algorithm == "rl_td_learning_train_solve":
            self.is_running_animation = False
            self.complex_results_scroll_y = 0
            self.run_td_value_prediction()
            self.current_state = self.initial_state[:]  # Reset current state
            self.draw()  # Update display after training

            if self.v_table and not self.app_should_quit:
                self.current_state = self.initial_state[:]  # Ensure starting from initial
                path_from_v_policy = self.generate_path_from_v_values(self.initial_state[:])
                if path_from_v_policy:
                    self.solution_path = path_from_v_policy
                    self.complex_search_result_text += f"\nPath generated from learned V-values (length {len(self.solution_path) - 1})."
                    if self.solution_path and self.solution_path[-1] == self.goal_state_1d:
                        self.is_running_animation = True
                        self.current_state = self.solution_path[0]  # Start animation
                    else:
                        self.complex_search_result_text += "\nDerived policy did not reach the goal."
                        self.is_running_animation = False
                else:
                    self.complex_search_result_text += "\nCould not generate a path from learned V-values."
                    self.is_running_animation = False
            else:
                self.complex_search_result_text += "\nTD Value prediction did not run or V-table is empty."
                self.is_running_animation = False
            self.needs_reset = True
            self.draw()

        elif self.algorithm:
            self.is_running_animation = True
            algo_map = {"bfs": self.bfs, "dfs": self.dfs, "ucs": self.ucs, "ids": self.ids, "greedy": self.greedy,
                        "astar": self.astar, "ida": self.ida,
                        "simplehc": self.simple_hill_climbing, "steepesthc": self.steepest_hill_climbing,
                        "stochastichc": self.stochastic_hill_climbing,
                        "simanneal": self.simulated_annealing, "genetic": self.genetic_algorithm,
                        "beam": self.beam_search}
            if self.algorithm in algo_map:
                self.solution_path = algo_map[self.algorithm](current_initial, goal_target)

            if not self.solution_path and not self.app_should_quit:
                messagebox.showerror("No Solution", f"No solution for {self.algorithm.upper()}.")
                self.is_running_animation = False  # Stop animation if no solution
            elif self.app_should_quit:
                self.is_running_animation = False  # Stop animation if user quit
                self.solution_path = []  # Clear path if quit
            self.needs_reset = True
        else:
            messagebox.showerror("Error", "Algorithm not selected/recognized.")
            self.needs_reset = False  # No need to reset if no algo was run

        self.solve_time = time.time() - start_time
        self.running_action_text = None
        self.draw()

    def format_state_for_display(self, state_1d_list):
        if not state_1d_list or len(state_1d_list) != 9: return "[Invalid State]"
        return f"[{state_1d_list[0:3]}, {state_1d_list[3:6]}, {state_1d_list[6:9]}]"

    def get_possible_moves_with_names(self, state_1d):
        moves = []
        zero_idx = state_1d.index(0) if 0 in state_1d else -1
        if zero_idx == -1: return []
        r, c = zero_idx // 3, zero_idx % 3
        pot_moves = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]
        for dr, dc, name in pot_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_s = state_1d[:]
                tile_to_move = nr * 3 + nc
                new_s[zero_idx], new_s[tile_to_move] = new_s[tile_to_move], new_s[zero_idx]
                moves.append((new_s, name))
        return moves

    def generate_and_or_plan_text(self, initial_state):
        text = f"AND-OR Search (Conceptual Plan):\n\nInitial: {self.format_state_for_display(initial_state)}\nGoal: {self.format_state_for_display(self.goal_state_1d)}\n\nPrinciple: Handles non-deterministic actions.\n"
        return text

    def generate_sensorless_plan_text(self, initial_state):
        return f"Sensorless Search (Conceptual Plan):\n\nInitial (Context): {self.format_state_for_display(initial_state)}\n..."

    def generate_partially_observable_plan_text(self, initial_state):
        return f"Partially Observable Search (Conceptual Plan):\n\nInitial (Context): {self.format_state_for_display(initial_state)}\n..."

    def animate_solution_step(self):
        if self.is_running_animation and self.solution_path and self.current_step < len(self.solution_path):
            self.current_state = self.solution_path[self.current_step]
            self.current_step += 1
        else:
            self.is_running_animation = False

    def reset_all(self):
        if self.is_q_learning_training_active:
            messagebox.showinfo("Information", "Cannot reset while Q-Learning training is active.", parent=self.root)
            return
        self.running_action_text = "Reset"
        self.draw()
        pygame.time.wait(100)
        self.is_running_animation = False
        self.current_step = 0
        self.solution_path = []
        self.current_state = self.initial_state.copy()
        self.solve_time = 0
        self.selected_algo = None
        self.algorithm = None
        self.needs_reset = False
        self.complex_search_result_text = ""
        self.complex_actual_initial_state = None
        self.complex_use_default_setup = True
        self.scroll_y_main = 0
        self.complex_results_scroll_y = 0
        self.q_table = {}
        self.v_table = {}
        self.q_learning_trained = False
        # self.is_q_learning_training_active = False # Should already be false if not training
        self.app_should_quit = False  # Reset quit flag
        self.active_simulation = None
        self.running_action_text = None
        self.draw()

    async def show_solution_path_standard(self):
        if self.is_q_learning_training_active or self.app_should_quit: return
        is_constrained_algo = self.algorithm and (
                "bp_25adj" in self.algorithm or "fc_25adj" in self.algorithm or "mc_25adj_repair" in self.algorithm)

        if self.algorithm and self.algorithm in ["and_or_sim", "non_obs_sim",
                                                 "partially_obs_sim"] and not is_constrained_algo:
            messagebox.showinfo("Not Applicable", "This option is for standard or constrained pathfinding algorithms.",
                                parent=self.root)
            return
        if self.algorithm == "rl_q_learning_train_solve" and not (
                self.solution_path and self.solution_path[-1] == self.goal_state_1d):
            messagebox.showwarning("Warning", "No successful solution from Q-Learning.", parent=self.root)
            return
        if self.algorithm == "rl_td_learning_train_solve" and not (
                self.solution_path and self.solution_path[-1] == self.goal_state_1d):
            messagebox.showwarning("Warning", "No successful solution from TD Learning.", parent=self.root)
            return
        if not self.solution_path:
            messagebox.showwarning("Warning", "No solution available.", parent=self.root)
            return

        self.running_action_text = "Solution"
        self.is_showing_solution_window = True  # Đặt cờ
        self.draw()  # Vẽ màn hình chính một lần
        await asyncio.sleep(0.05)  # Chờ một chút

        num_steps = len(self.solution_path)
        max_cols = 5
        tile_sz = 40
        # if num_steps <= 0: return # Đã kiểm tra ở trên
        num_cols = min(max_cols, num_steps)
        num_rows = (num_steps + num_cols - 1) // num_cols
        board_w, board_h, pad = tile_sz * 3, tile_sz * 3 + 30, 40

        current_main_screen_w, current_main_screen_h = self.screen.get_size()
        win_w = min(num_cols * (board_w + pad) + pad, current_main_screen_w - 50)
        win_h = min(num_rows * (board_h + pad) + pad, current_main_screen_h - 50)
        win_w = max(300, win_w)
        win_h = max(300, win_h)

        sol_screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
        pygame.display.set_caption("Solution Path")
        running, scroll_y, total_h = True, 0, num_rows * (board_h + pad) + pad

        try:
            while running:
                if self.app_should_quit: running = False; break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: self.app_should_quit = True; running = False; break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 4:
                            scroll_y = min(scroll_y + 40, 0)
                        elif event.button == 5 and total_h > win_h:
                            scroll_y = max(scroll_y - 40, win_h - total_h)
                    if event.type == pygame.VIDEORESIZE:
                        win_w, win_h = event.w, event.h
                        sol_screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
                        scroll_y = max(scroll_y, win_h - total_h) if total_h > win_h else 0
                if not running: break

                sol_screen.fill((60, 60, 60))
                for i, state in enumerate(self.solution_path):
                    r_idx, c_idx = i // num_cols, i % num_cols
                    x, y = pad + c_idx * (board_w + pad), pad + r_idx * (board_h + pad) + scroll_y
                    if y + board_h + pad > 0 and y < win_h:
                        self.draw_board(sol_screen, state, x, y, f"Step {i}", tile_sz)
                pygame.display.flip()
                await asyncio.sleep(1.0 / FPS if platform.system() == "Emscripten" else 0.01)
        finally:
            self.is_showing_solution_window = False  # Reset cờ
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            pygame.display.set_caption("8-Puzzle Solver")
            self.running_action_text = None
            self.draw()  # Vẽ lại màn hình chính

    @staticmethod
    def get_neighbors(state):
        neighbors = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        zero_idx = state.index(0) if 0 in state else -1
        if zero_idx == -1: return []
        r, c = zero_idx // 3, zero_idx % 3
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                new_s = state[:]
                tile_idx = nr * 3 + nc
                new_s[zero_idx], new_s[tile_idx] = new_s[tile_idx], new_s[zero_idx]
                neighbors.append(new_s)
        return neighbors

    @staticmethod
    def is_solvable(state, goal):
        inv_s = [x for x in state if x != 0]
        inversions = 0
        for i in range(len(inv_s)):
            for j in range(i + 1, len(inv_s)):
                if inv_s[i] > inv_s[j]: inversions += 1
        return inversions % 2 == 0

    def manhattan_distance(self, state, goal):
        dist = 0
        for i in range(9):
            if state[i] != 0:
                val = state[i]
                r, c = i // 3, i % 3
                goal_idx = goal.index(val) if val in goal else -1
                if goal_idx == -1: return float('inf')
                gr, gc = goal_idx // 3, goal_idx % 3
                dist += abs(r - gr) + abs(c - gc)
        return dist

    def bfs(self, initial, goal):
        if not self.is_solvable(initial, goal): return []
        queue = deque([(initial, [initial])])
        visited = {tuple(initial)}
        count = 0
        while queue:
            count += 1
            if self.app_should_quit: return []
            if count % 2000 == 0:  # Check for quit event periodically
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.app_should_quit = True
                        return []  # Exit if quit
            state, path = queue.popleft()
            if state == goal: return path
            for neighbor in self.get_neighbors(state):
                if tuple(neighbor) not in visited:
                    visited.add(tuple(neighbor))
                    queue.append((neighbor, path + [neighbor]))
        return []

    def dfs(self, initial, goal):
        if not self.is_solvable(initial, goal): return []
        stack = [(initial, [initial], 0)]
        visited = {tuple(initial)}
        max_depth = 30  # Consider making this adjustable or dynamic
        count = 0
        while stack:
            if self.app_should_quit: return []
            count += 1
            if count % 1000 == 0:  # Check for quit event periodically
                for e_event in pygame.event.get():  # Use a different variable name
                    if e_event.type == pygame.QUIT:
                        self.app_should_quit = True
                        return []  # Exit if quit
            state, path, depth = stack.pop()
            if state == goal: return path
            if depth >= max_depth: continue
            neighbors = self.get_neighbors(state)
            random.shuffle(neighbors)  # For some variation in DFS
            for neighbor in neighbors:
                if tuple(neighbor) not in visited:
                    visited.add(tuple(neighbor))
                    stack.append((neighbor, path + [neighbor], depth + 1))
        return []

    def ucs(self, initial, goal):
        if not self.is_solvable(initial, goal): return []
        pq = [(0, initial, [initial])]  # (cost, state, path)
        visited_costs = {tuple(initial): 0}
        count = 0
        while pq:
            if self.app_should_quit: return []
            count += 1
            if count % 1000 == 0:  # Check for quit event periodically
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT:
                        self.app_should_quit = True
                        return []
            cost, state, path = heapq.heappop(pq)
            if state == goal: return path
            if cost > visited_costs.get(tuple(state), float('inf')): continue  # Already found shorter path
            for neighbor in self.get_neighbors(state):
                new_cost = cost + 1  # Assuming cost of each move is 1
                if new_cost < visited_costs.get(tuple(neighbor), float('inf')):
                    visited_costs[tuple(neighbor)] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))
        return []

    def ids(self, initial, goal):
        if not self.is_solvable(initial, goal): return []

        def dls(curr, pth, lim, visited_tuples_in_path, call_count_arr):  # Pass visited set for current path
            call_count_arr[0] += 1
            if self.app_should_quit: return None
            if call_count_arr[0] % 2000 == 0:
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT:
                        self.app_should_quit = True
                        return None
            if curr == goal: return pth
            if lim == 0: return None
            for neigh in self.get_neighbors(curr):
                if tuple(neigh) not in visited_tuples_in_path:  # Check only against current path to avoid cycles
                    res = dls(neigh, pth + [neigh], lim - 1, visited_tuples_in_path | {tuple(neigh)}, call_count_arr)
                    if res: return res
            return None

        for depth in range(31):  # Max depth for IDS
            if self.app_should_quit: return []
            # For each DLS call, visited should only track nodes in the current path to avoid cycles
            result = dls(initial, [initial], depth, {tuple(initial)}, [0])
            if result: return result
        return []

    def astar(self, initial, goal):
        if not self.is_solvable(initial, goal): return []
        g = 0
        h = self.manhattan_distance(initial, goal)
        f = g + h
        pq = [(f, g, initial, [initial])]  # (f_cost, g_cost, state, path)
        visited_g = {tuple(initial): g}  # Store g_cost for visited states
        count = 0
        while pq:
            if self.app_should_quit: return []
            count += 1
            if count % 1000 == 0:
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT:
                        self.app_should_quit = True
                        return []
            _f, g_curr, state, path = heapq.heappop(pq)
            if state == goal: return path
            if g_curr > visited_g.get(tuple(state), float('inf')): continue  # Found a shorter path already
            for neighbor in self.get_neighbors(state):
                new_g = g_curr + 1
                if new_g < visited_g.get(tuple(neighbor), float('inf')):
                    visited_g[tuple(neighbor)] = new_g
                    h_new = self.manhattan_distance(neighbor, goal)
                    heapq.heappush(pq, (new_g + h_new, new_g, neighbor, path + [neighbor]))
        return []

    def greedy(self, initial, goal):
        if not self.is_solvable(initial, goal): return []
        pq = [(self.manhattan_distance(initial, goal), initial, [initial])]  # (h_cost, state, path)
        visited = {tuple(initial)}
        count = 0
        while pq:
            if self.app_should_quit: return []
            count += 1
            if count % 1000 == 0:
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT:
                        self.app_should_quit = True
                        return []
            _, state, path = heapq.heappop(pq)
            if state == goal: return path
            # Get neighbors, calculate their h_cost, and add to pq if not visited
            for neighbor_state in self.get_neighbors(state):
                if tuple(neighbor_state) not in visited:
                    visited.add(tuple(neighbor_state))
                    h_val = self.manhattan_distance(neighbor_state, goal)
                    heapq.heappush(pq, (h_val, neighbor_state, path + [neighbor_state]))
        return []

    def ida(self, initial, goal):
        if not self.is_solvable(initial, goal): return []

        def search(pth, g_cost, threshold, call_count_arr):
            call_count_arr[0] += 1
            if self.app_should_quit: return None, threshold
            if call_count_arr[0] % 2000 == 0:
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT:
                        self.app_should_quit = True
                        return None, threshold

            state = pth[-1]
            h = self.manhattan_distance(state, goal)
            f = g_cost + h
            if f > threshold: return None, f  # Prune if f exceeds threshold
            if state == goal: return pth, f  # Goal found

            min_f_overall = float('inf')
            # Sort neighbors by their f-cost to explore promising ones first (optional but can help)
            sorted_neighbors = sorted(
                self.get_neighbors(state),
                key=lambda n: g_cost + 1 + self.manhattan_distance(n, goal)
            )

            for neigh in sorted_neighbors:
                if neigh not in pth:  # Avoid cycles in the current path
                    res, new_f_val = search(pth + [neigh], g_cost + 1, threshold, call_count_arr)
                    if self.app_should_quit: return None, threshold
                    if res: return res, new_f_val  # Propagate solution
                    min_f_overall = min(min_f_overall, new_f_val)  # Update min f-cost found beyond threshold
            return None, min_f_overall

        current_threshold = self.manhattan_distance(initial, goal)
        while True:
            if self.app_should_quit: return []
            # For each iteration, the path starts fresh
            result_path, next_threshold = search([initial], 0, current_threshold, [0])
            if self.app_should_quit: return []
            if result_path: return result_path  # Solution found
            if next_threshold == float('inf'): return []  # No solution found, all paths explored
            if next_threshold <= current_threshold: return []  # Should not happen if logic is correct, but a safeguard
            current_threshold = next_threshold

    def simple_hill_climbing(self, initial, goal, max_iter=1000):
        if not self.is_solvable(initial, goal): return []
        curr = initial
        path = [curr]
        for iter_count in range(max_iter):
            if iter_count % 100 == 0:
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT: self.app_should_quit = True
                if self.app_should_quit: return []

            if curr == goal: return path
            curr_h = self.manhattan_distance(curr, goal)
            moved = False
            # Explore neighbors in a random order
            neighbors = self.get_neighbors(curr)
            random.shuffle(neighbors)
            for neigh in neighbors:
                if self.manhattan_distance(neigh, goal) < curr_h:
                    curr = neigh
                    path.append(curr)
                    moved = True
                    break  # Move to the first better neighbor found
            if not moved: break  # Stuck in local optimum or plateau
        return path if curr == goal else []

    def steepest_hill_climbing(self, initial, goal, max_iter=1000):
        if not self.is_solvable(initial, goal): return []
        curr = initial
        path = [curr]
        for iter_count in range(max_iter):
            if iter_count % 100 == 0:
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT: self.app_should_quit = True
                if self.app_should_quit: return []

            if curr == goal: return path
            curr_h = self.manhattan_distance(curr, goal)
            neighs = self.get_neighbors(curr)
            if not neighs: break  # No neighbors

            best_n = None
            best_h = curr_h
            # Find the steepest descent neighbor
            for n_state in neighs:
                n_h = self.manhattan_distance(n_state, goal)
                if n_h < best_h:
                    best_h = n_h
                    best_n = n_state

            if best_n is None or best_h >= curr_h:  # No better neighbor found
                break
            curr = best_n
            path.append(curr)
        return path if curr == goal else []

    def stochastic_hill_climbing(self, initial, goal, max_iter=1000):
        if not self.is_solvable(initial, goal): return []
        curr = initial
        path = [curr]
        for iter_count in range(max_iter):
            if iter_count % 100 == 0:
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT: self.app_should_quit = True
                if self.app_should_quit: return []

            if curr == goal: return path
            curr_h = self.manhattan_distance(curr, goal)
            # Get all neighbors better than current
            better_neighbors = [n for n in self.get_neighbors(curr) if self.manhattan_distance(n, goal) < curr_h]
            if not better_neighbors: break  # No better neighbors
            curr = random.choice(better_neighbors)  # Choose one stochastically
            path.append(curr)
        return path if curr == goal else []

    def simulated_annealing(self, initial, goal, temp_start=500.0, cool_rate=0.999, max_iter=20000, restarts=5):
        if not self.is_solvable(initial, goal): return []
        best_s = initial
        min_h = self.manhattan_distance(initial, goal)
        if min_h == 0: return [initial]

        for restart_num in range(restarts):
            if self.app_should_quit: return []

            curr_s = initial if restart_num == 0 else self.random_state()
            curr_h = self.manhattan_distance(curr_s, goal)

            if curr_h < min_h:
                min_h = curr_h
                best_s = curr_s

            if curr_h == 0:
                best_s = curr_s
                break

            temp = temp_start
            iterations_per_restart = max_iter // restarts

            for i in range(iterations_per_restart):
                if i % 100 == 0:
                    for e_event in pygame.event.get():
                        if e_event.type == pygame.QUIT:
                            self.app_should_quit = True
                    if self.app_should_quit:
                        return []

                if curr_h == 0:
                    best_s = curr_s
                    break

                neighs = self.get_neighbors(curr_s)
                if not neighs: break

                next_s = random.choice(neighs)
                next_h = self.manhattan_distance(next_s, goal)
                delta_e = next_h - curr_h

                if delta_e < 0 or (temp > 0.001 and random.random() < math.exp(-delta_e / temp)):
                    curr_s, curr_h = next_s, next_h
                    if curr_h < min_h:
                        min_h = curr_h
                        best_s = curr_s

                temp *= cool_rate
                if temp < 0.001 and i > iterations_per_restart // 2:
                    break

            if best_s == goal:
                break

        return self.astar(initial, best_s) if best_s == goal else []

    def genetic_algorithm(self, initial, goal, pop_size=50, mut_rate=0.1, max_gen=100, elite_size=10):
        if not self.is_solvable(initial, goal): return []

        pop = [initial] + [self.random_state() for _ in range(pop_size - 1)]

        best_overall_individual = initial
        best_overall_fitness = -self.manhattan_distance(initial, goal)

        for gen_count in range(max_gen):
            if gen_count % 2 == 0:
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT:
                        self.app_should_quit = True
                if self.app_should_quit:
                    return []

            pop_with_fitness = []
            for ind in pop:
                fitness = -self.manhattan_distance(ind, goal)
                pop_with_fitness.append((ind, fitness))

            pop_with_fitness.sort(key=lambda x: x[1], reverse=True)

            if pop_with_fitness[0][1] > best_overall_fitness:
                best_overall_fitness = pop_with_fitness[0][1]
                best_overall_individual = pop_with_fitness[0][0]

            if best_overall_individual == goal:
                return self.astar(initial, best_overall_individual)

            new_pop = []
            actual_elite_size = min(elite_size, len(pop_with_fitness))
            for i in range(actual_elite_size):
                new_pop.append(pop_with_fitness[i][0])

            while len(new_pop) < pop_size:
                idx1 = random.randrange(len(pop_with_fitness) // 2 if len(pop_with_fitness) > 1 else 1)
                idx2 = random.randrange(len(pop_with_fitness) // 2 if len(pop_with_fitness) > 1 else 1)
                p1 = pop_with_fitness[idx1][0]
                p2 = pop_with_fitness[idx2][0]

                child = self.crossover(p1, p2)

                if random.random() < mut_rate:
                    child = self.mutate(child)

                if self.is_solvable(child, goal):
                    new_pop.append(child)
                else:
                    new_pop.append(self.random_state())

            pop = new_pop

        return self.astar(initial, best_overall_individual) if best_overall_individual == goal else []

    def random_state(self):
        while True:
            state = list(range(9))
            random.shuffle(state)
            if self.is_solvable(state, self.goal_state_1d):
                return state

    def crossover(self, p1, p2):
        child = [-1] * 9
        start, end = sorted(random.sample(range(9), 2))

        child[start:end + 1] = p1[start:end + 1]

        p1_segment_set = set(child[start:end + 1])
        p2_elements_to_add = []

        for i in range(9):
            current_p2_idx = (end + 1 + i) % 9
            val = p2[current_p2_idx]
            if val not in p1_segment_set:
                p2_elements_to_add.append(val)

        child_fill_idx = 0
        for i in range(9):
            current_child_fill_spot = (end + 1 + i) % 9
            if child[current_child_fill_spot] == -1:
                if child_fill_idx < len(p2_elements_to_add):
                    child[current_child_fill_spot] = p2_elements_to_add[child_fill_idx]
                    child_fill_idx += 1

        if len(set(child)) != 9 or -1 in child:
            return self.random_state()

        return child

    def mutate(self, state):
        s = state[:]
        i1, i2 = random.sample(range(9), 2)
        s[i1], s[i2] = s[i2], s[i1]
        return s

    def beam_search(self, initial, goal, beam_width=5):
        if not self.is_solvable(initial, goal): return []
        beam = [(self.manhattan_distance(initial, goal), initial, [initial])]  # (h_cost, state, path)
        visited_beam = {tuple(initial)}  # Keep track of states in the beam or previously in beam

        for _ in range(50):  # Max iterations/depth for beam search
            if self.app_should_quit: return []

            candidates = []
            # Generate all possible next states from current beam states
            for _h, s, pth in beam:
                if s == goal: return pth  # Goal found
                for n in self.get_neighbors(s):
                    # Add to candidates if not already visited (to avoid re-expanding same state in current beam generation)
                    if tuple(n) not in visited_beam:  # Check against all visited states in beam search
                        candidates.append((self.manhattan_distance(n, goal), n, pth + [n]))

            if not candidates: break  # No more candidates to explore

            # Sort candidates by heuristic and select top 'beam_width'
            # Add newly selected states to visited_beam
            new_beam = []
            # Use a temporary set to avoid duplicates within the new_beam before adding to global visited_beam
            states_for_new_beam_tuples = set()

            for h_c, s_c, p_c in sorted(candidates, key=lambda item: item[0]):
                if len(new_beam) < beam_width:
                    s_c_tuple = tuple(s_c)
                    if s_c_tuple not in states_for_new_beam_tuples:  # Ensure unique states in the new beam
                        new_beam.append((h_c, s_c, p_c))
                        states_for_new_beam_tuples.add(s_c_tuple)
                        visited_beam.add(s_c_tuple)  # Add to global visited set
                else:
                    break  # Beam is full

            beam = new_beam
            if not beam: break  # No states left in beam

        return []  # Goal not found within iterations

    def check_2_5_adjacency(self, state_list_1d):
        if len(state_list_1d) != 9: return False
        state_2d = [state_list_1d[i * 3:(i + 1) * 3] for i in range(3)]
        pos2 = None
        pos5 = None
        for r_idx in range(3):
            for c_idx in range(3):
                if state_2d[r_idx][c_idx] == 2:
                    pos2 = (r_idx, c_idx)
                elif state_2d[r_idx][c_idx] == 5:
                    pos5 = (r_idx, c_idx)

        if pos2 is None or pos5 is None:
            return False

        return abs(pos2[0] - pos5[0]) <= 1 and abs(pos2[1] - pos5[1]) <= 1

    def get_neighbors_8puzzle_constrained(self, state_1d_list):
        standard_neighbors_data = self.get_possible_moves_with_names(state_1d_list)
        constrained_neighbors = []
        for move_data in standard_neighbors_data:
            neighbor_state_list = move_data[0]
            if self.check_2_5_adjacency(neighbor_state_list):
                constrained_neighbors.append(neighbor_state_list)
        return constrained_neighbors

    def backtracking_8puzzle_constrained(self, initial_state_1d, goal_state_1d, max_depth=30):
        if not self.check_2_5_adjacency(initial_state_1d):
            self.complex_search_result_text = "Error: Initial state violates 2 & 5 adjacency constraint."
            return []
        if not self.check_2_5_adjacency(goal_state_1d):
            self.complex_search_result_text = "Error: Goal state violates 2 & 5 adjacency constraint."
            return []

        start_node_tuple = tuple(initial_state_1d)
        end_node_tuple = tuple(goal_state_1d)

        stack = [(start_node_tuple, [initial_state_1d], 0)]  # (state_tuple, path_list, depth)

        count = 0
        while stack:
            if self.app_should_quit: return []
            count += 1
            if count % 2000 == 0:  # Periodically check for quit event
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT:
                        self.app_should_quit = True
                        return []

            current_node_tuple, current_path_list, depth = stack.pop()

            if current_node_tuple == end_node_tuple:
                return current_path_list

            if depth >= max_depth:
                continue

            current_node_list_for_neighbors = list(current_node_tuple)
            neighbors_states_list = self.get_neighbors_8puzzle_constrained(current_node_list_for_neighbors)

            # To avoid cycles in the current path
            path_tuples_set = {tuple(s) for s in current_path_list}

            for neighbor_state_list in reversed(
                    neighbors_states_list):  # Explore in a consistent order (e.g., reverse for LIFO stack)
                neighbor_state_tuple = tuple(neighbor_state_list)
                if neighbor_state_tuple not in path_tuples_set:
                    new_path_list = current_path_list + [neighbor_state_list]
                    stack.append((neighbor_state_tuple, new_path_list, depth + 1))
        return []

    def forward_checking_8puzzle_constrained(self, initial_state_1d, goal_state_1d, max_depth=30):
        if not self.check_2_5_adjacency(initial_state_1d):
            self.complex_search_result_text = "Error: Initial state violates 2 & 5 adjacency constraint."
            return []
        if not self.check_2_5_adjacency(goal_state_1d):
            self.complex_search_result_text = "Error: Goal state violates 2 & 5 adjacency constraint."
            return []

        start_node_tuple = tuple(initial_state_1d)
        end_node_tuple = tuple(goal_state_1d)

        # Helper for forward checking: can we reach the goal from this node without violating constraints?
        # This is a simplified check for this context, a full FC would prune domains.
        # Here, we just check if there's at least one valid next move not in the current path.
        def check_forward_8puzzle_fc(node_to_check_list, visited_on_branch_set_tuples_fc):
            potential_next_moves = self.get_neighbors_8puzzle_constrained(node_to_check_list)
            for next_potential_state_list_fc in potential_next_moves:
                if tuple(next_potential_state_list_fc) not in visited_on_branch_set_tuples_fc:
                    return True  # At least one valid, unvisited move exists
            return False  # No valid, unvisited moves from here

        memo_fc = {}  # Memoization for FC states

        def solve_fc_recursive(current_node_list_fc, current_path_list_of_lists_fc, visited_on_branch_set_tuples_fc,
                               depth_fc):
            # Create a hashable key for memoization
            # frozenset for visited_on_branch_set_tuples_fc makes it hashable
            state_key = (tuple(current_node_list_fc), frozenset(visited_on_branch_set_tuples_fc), depth_fc)
            if state_key in memo_fc:
                return memo_fc[state_key]

            if self.app_should_quit: return []
            if depth_fc % 100 == 0:  # Check for quit event periodically
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT: self.app_should_quit = True
                if self.app_should_quit: return []

            current_node_tuple_fc = tuple(current_node_list_fc)
            if current_node_tuple_fc == end_node_tuple:
                return current_path_list_of_lists_fc

            if depth_fc >= max_depth:
                return []

            neighbors_states_list_fc = self.get_neighbors_8puzzle_constrained(current_node_list_fc)

            for neighbor_state_list_fc in neighbors_states_list_fc:
                neighbor_state_tuple_fc = tuple(neighbor_state_list_fc)

                if neighbor_state_tuple_fc not in visited_on_branch_set_tuples_fc:
                    # Forward Check:
                    # For this simplified version, we ensure the neighbor itself is valid and
                    # there's a path forward from it (not strictly domain pruning of CSPs)
                    new_visited_for_forward_check = visited_on_branch_set_tuples_fc | {neighbor_state_tuple_fc}

                    # The check_2_5_adjacency is already done by get_neighbors_8puzzle_constrained
                    # The check_forward_8puzzle_fc is a lookahead to see if it gets stuck immediately
                    if check_forward_8puzzle_fc(neighbor_state_list_fc,
                                                new_visited_for_forward_check) or neighbor_state_tuple_fc == end_node_tuple:
                        new_path_fc = current_path_list_of_lists_fc + [neighbor_state_list_fc]
                        result_fc = solve_fc_recursive(neighbor_state_list_fc, new_path_fc,
                                                       new_visited_for_forward_check, depth_fc + 1)
                        if result_fc:
                            memo_fc[state_key] = result_fc
                            return result_fc

            memo_fc[state_key] = []  # No solution from this state with current path/depth
            return []

        initial_path_fc = [initial_state_1d]
        initial_visited_fc = {start_node_tuple}  # Set of tuples for visited states in current path
        return solve_fc_recursive(initial_state_1d, initial_path_fc, initial_visited_fc, 0)

    def _count_conflicts_for_mc_report(self, path_states_list_mc):
        conflicts = 0
        if not path_states_list_mc: return float('inf')

        # Constraint 1: Each state in the path must satisfy 2-5 adjacency
        for state_mc in path_states_list_mc:
            if not self.check_2_5_adjacency(state_mc):
                conflicts += 10  # Higher penalty for violating state constraint

        # Constraint 2: Consecutive states in the path must be valid moves
        for i_mc in range(len(path_states_list_mc) - 1):
            p_i_mc = path_states_list_mc[i_mc]
            p_i_plus_1_mc = path_states_list_mc[i_mc + 1]

            # get_neighbors returns states reachable by one standard 8-puzzle move
            possible_next_states_from_pi_mc = [s_mc for s_mc in self.get_neighbors(p_i_mc)]

            is_connected_mc = False
            for s_next_mc in possible_next_states_from_pi_mc:
                if tuple(s_next_mc) == tuple(p_i_plus_1_mc):
                    is_connected_mc = True
                    break
            if not is_connected_mc:
                conflicts += 1  # Penalty for invalid transition
        return conflicts

    def min_conflicts_8puzzle_repair_constrained(self, initial_path_list_of_lists_mc, max_steps_mc=100):
        if not initial_path_list_of_lists_mc:
            self.complex_search_result_text += "\nError: Initial path is empty for Min-Conflicts."
            return []

        current_path_mc = [list(state_mc) for state_mc in initial_path_list_of_lists_mc]

        for step_mc in range(max_steps_mc):
            if self.app_should_quit: break
            if step_mc % 20 == 0:  # Check for quit event periodically
                for e_event in pygame.event.get():
                    if e_event.type == pygame.QUIT: self.app_should_quit = True
                if self.app_should_quit: break

            num_current_conflicts_mc = self._count_conflicts_for_mc_report(current_path_mc)
            if num_current_conflicts_mc == 0 and current_path_mc[-1] == self.goal_state_1d:  # Ensure goal is also met
                self.complex_search_result_text += f"\nMin-Conflicts: Path successfully repaired in {step_mc} steps."
                return current_path_mc

            # Identify all conflicted variables (indices in the path)
            conflicted_indices_mc = []
            for i_mc, state_mc in enumerate(current_path_mc):
                if not self.check_2_5_adjacency(state_mc):
                    conflicted_indices_mc.append(i_mc)
            for i_mc in range(len(current_path_mc) - 1):
                p_i_mc = current_path_mc[i_mc]
                p_i_plus_1_mc = current_path_mc[i_mc + 1]
                if tuple(p_i_plus_1_mc) not in [tuple(n) for n in self.get_neighbors(p_i_mc)]:
                    if i_mc not in conflicted_indices_mc: conflicted_indices_mc.append(i_mc)
                    if i_mc + 1 not in conflicted_indices_mc: conflicted_indices_mc.append(i_mc + 1)

            if not conflicted_indices_mc:  # No conflicts but not at goal, or goal state itself is invalid (unlikely if initial checks pass)
                if current_path_mc[-1] != self.goal_state_1d:
                    # Try to make a move from the last state towards the goal if possible
                    # This part is a heuristic, might need more sophisticated handling
                    last_state = current_path_mc[-1]
                    neighbors_of_last = self.get_neighbors_8puzzle_constrained(last_state)
                    if neighbors_of_last:
                        # Prefer a neighbor that reduces Manhattan distance to goal
                        neighbors_of_last.sort(key=lambda s: self.manhattan_distance(s, self.goal_state_1d))
                        if self.manhattan_distance(neighbors_of_last[0], self.goal_state_1d) < self.manhattan_distance(
                                last_state, self.goal_state_1d):
                            current_path_mc.append(neighbors_of_last[0])  # Extend path
                            continue  # Re-evaluate conflicts
                # If still no conflicts and not at goal, it might be stuck.
                # Or if goal is reached but has conflicts (e.g. 2-5 constraint on goal itself)
                # For now, let it continue to see if random choices help, or break if stuck.
                if num_current_conflicts_mc > 0:  # If goal has conflicts
                    pass  # Let it try to fix the goal state if it's in conflicted_indices_mc
                else:  # No conflicts, but not at goal, and couldn't extend path
                    break  # Stuck

            var_index_to_fix_mc = random.choice(conflicted_indices_mc) if conflicted_indices_mc else -1
            if var_index_to_fix_mc == -1: continue  # Should not happen if conflicted_indices_mc is not empty

            state_to_fix_mc = current_path_mc[var_index_to_fix_mc]
            best_alternative_state_mc = state_to_fix_mc  # Default to current
            min_conflicts_after_change_mc = num_current_conflicts_mc

            # Try all valid neighbors of the state_to_fix_mc (or states around it)
            # For simplicity, let's try neighbors of the current state at var_index_to_fix_mc
            # This is a greedy one-step lookahead.
            potential_alternatives_mc = self.get_neighbors(state_to_fix_mc)  # Standard neighbors
            random.shuffle(potential_alternatives_mc)

            for alt_state_list_mc in potential_alternatives_mc:
                original_state_at_index_mc = list(current_path_mc[var_index_to_fix_mc])
                current_path_mc[var_index_to_fix_mc] = alt_state_list_mc  # Try assigning the alternative

                conflicts_with_alt_mc = self._count_conflicts_for_mc_report(current_path_mc)

                if conflicts_with_alt_mc < min_conflicts_after_change_mc:
                    min_conflicts_after_change_mc = conflicts_with_alt_mc
                    best_alternative_state_mc = list(alt_state_list_mc)

                # Revert for next iteration if this alternative is not chosen
                current_path_mc[var_index_to_fix_mc] = original_state_at_index_mc

            current_path_mc[var_index_to_fix_mc] = best_alternative_state_mc  # Make the best change found

        final_conflicts = self._count_conflicts_for_mc_report(current_path_mc)
        if final_conflicts == 0 and current_path_mc[-1] == self.goal_state_1d:
            self.complex_search_result_text += f"\nMin-Conflicts: Path successfully repaired after {max_steps_mc} steps (or earlier)."
        else:
            self.complex_search_result_text += f"\nMin-Conflicts: Could not repair all conflicts after {max_steps_mc} steps. Remaining conflicts: {final_conflicts}."
            if current_path_mc[-1] != self.goal_state_1d:
                self.complex_search_result_text += f" Path does not end at goal."
        return current_path_mc

    async def main_loop(self):
        # self.draw() # Initial draw is handled by the loop now
        app_is_running = True
        while app_is_running:
            if self.app_should_quit: app_is_running = False; break
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app_should_quit = True
                    app_is_running = False
                    break

                if self.is_showing_solution_window:
                    # Event handling for solution window is inside show_solution_path_standard
                    pass
                else:
                    # Event handling for the main application window
                    if self.active_simulation:
                        self.active_simulation.handle_event(event, mouse_pos)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.scrollable_area_y_start <= mouse_pos[
                            1] < self.screen_height:  # Check if click is in button area
                            if event.button == 4:  # Scroll up for buttons
                                if self.scrollable_content_height > self.visible_scrollable_area_height:
                                    self.scroll_y_main = min(self.scroll_y_main + 30, 0)
                            elif event.button == 5:  # Scroll down for buttons
                                if self.scrollable_content_height > self.visible_scrollable_area_height:
                                    self.scroll_y_main = max(self.scroll_y_main - 30,
                                                             self.visible_scrollable_area_height - self.scrollable_content_height)
                        elif self.complex_results_panel_rect.collidepoint(mouse_pos) and not self.active_simulation:
                            # Scrolling for complex results panel
                            if event.button == 4:  # Scroll up
                                self.complex_results_scroll_y = min(self.complex_results_scroll_y + 20, 0)
                            elif event.button == 5:  # Scroll down
                                title_h = self.font.get_sized_height() + 20  # Approximate height of title
                                vis_text_h = self.complex_results_panel_rect.height - title_h
                                if self.complex_results_total_text_height > vis_text_h:
                                    max_scroll = vis_text_h - self.complex_results_total_text_height
                                    self.complex_results_scroll_y = max(self.complex_results_scroll_y - 20, max_scroll)

                        if event.button == 1 and not (
                                self.active_simulation and self.active_simulation.content_rect.collidepoint(mouse_pos)):
                            # Button click logic
                            button_allowed = not self.is_q_learning_training_active
                            if button_allowed:
                                mouse_y_rel_to_scroll_area = mouse_pos[1] - self.scrollable_area_y_start
                                mouse_y_rel_to_content = mouse_y_rel_to_scroll_area - self.scroll_y_main

                                for orig_rect, btn_text, callback, _group in self.buttons:
                                    # Check if click is within the original_rect's y-range relative to scrolled content
                                    if orig_rect.x <= mouse_pos[0] <= orig_rect.right and \
                                            orig_rect.y <= mouse_y_rel_to_content <= orig_rect.bottom:
                                        # Also ensure the button is visible on screen
                                        btn_on_screen_top = self.scrollable_area_y_start + orig_rect.y + self.scroll_y_main
                                        if btn_on_screen_top < self.screen_height and \
                                                btn_on_screen_top + orig_rect.height > self.scrollable_area_y_start and \
                                                self.scrollable_area_y_start <= mouse_pos[1] < self.screen_height:

                                            self.clicked_button_text = btn_text
                                            self.click_time = time.time()
                                            if callback:
                                                actual_func = callback
                                                if hasattr(callback, '__func__'):  # For methods
                                                    actual_func = callback.__func__

                                                if asyncio.iscoroutinefunction(actual_func):
                                                    asyncio.create_task(actual_func())
                                                else:
                                                    callback()
                                            break  # Button found and processed
                    if event.type == pygame.VIDEORESIZE:
                        if not self.is_showing_solution_window:  # Only resize main screen if solution window is not active
                            self.screen_width, self.screen_height = event.w, event.h
                            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                                                  pygame.RESIZABLE)
                            self._calculate_panel_rects()
                            if self.active_simulation:
                                self.active_simulation.content_rect = self.complex_results_panel_rect
                            # self.draw() # Draw will be called at the end of the loop
            if not app_is_running: break

            if not self.is_showing_solution_window:
                if self.active_simulation:
                    self.active_simulation.update()

                if self.is_running_animation and self.solution_path and \
                        (self.algorithm != "rl_q_learning_train_solve" or self.q_learning_trained):
                    self.animate_solution_step()

                self.draw()  # Draw main screen only if solution window is not active

            await asyncio.sleep(1.0 / FPS)


class AndOrSearchSim:
    def __init__(self, app_ref, content_rect):
        self.app_ref = app_ref
        self.content_rect = content_rect
        self.tile_font = app_ref.sim_tile_font_and_or
        self.status_font = app_ref.sim_status_font
        self.button_font = app_ref.sim_button_font
        self.puzzle_visual_width = SIM_GRID_SIZE * SIM_DISPLAY_TILE_SIZE_AND_OR
        self.puzzle_visual_height = SIM_GRID_SIZE * SIM_DISPLAY_TILE_SIZE_AND_OR
        self.margin_sim_area = 20
        self.sim_top_info_height = 80
        self.solve_button_rect = pygame.Rect(0, 0, 0, 0)
        self.solve_button_text_default = "Solve Next 'Easiest' Subgoal"
        self.animation_delay_per_step = 200
        self.status_message = "Initializing..."  # Initial status
        self.reset_simulation()

    def reset_simulation(self):
        self.puzzle_state = sim_generate_initial_states_standard_close(1, root_shuffles=random.randint(3, 6))[0]
        self.fixed_tiles = {}  # Tiles that are correctly placed and should not be moved by blank
        self.animation_path = []  # List of actions ['UP', 'DOWN', ...]
        self.current_anim_step = 0
        self.is_animating = False
        self.all_subgoals_completed = False
        self.current_target_tile_and_pos = None  # (tile_value, (target_r, target_c))
        self.status_message = "Ready. Click 'Solve' or 'R' to reset."
        self.determine_next_easiest_subgoal()

    def determine_next_easiest_subgoal(self):
        self.current_target_tile_and_pos = None
        min_dist_h = float('inf')
        easiest_tile_to_place = None

        # First, mark any tiles already in their correct fixed positions
        for tile_num_check in range(1, SIM_GRID_SIZE * SIM_GRID_SIZE):  # Exclude blank
            target_pos_check = SIM_TARGET_POSITIONS.get(tile_num_check)
            if not target_pos_check: continue
            current_pos_check = sim_get_tile_pos(self.puzzle_state, tile_num_check)
            if current_pos_check == target_pos_check and tile_num_check not in self.fixed_tiles:
                self.fixed_tiles[tile_num_check] = target_pos_check

        # Find the next tile to place (that is not fixed yet)
        # Prioritize tiles with smaller numbers first, then by heuristic
        for tile_num in range(1, SIM_GRID_SIZE * SIM_GRID_SIZE):  # Iterate 1 to 8
            target_pos = SIM_TARGET_POSITIONS.get(tile_num)
            if not target_pos: continue

            # If this tile is already fixed at its target, skip
            if tile_num in self.fixed_tiles and self.fixed_tiles[tile_num] == target_pos:
                continue

            curr_pos = sim_get_tile_pos(self.puzzle_state, tile_num)
            if not curr_pos: continue  # Should not happen if puzzle is valid

            # If tile is at target but not marked fixed, mark it and continue to find next *unfixed*
            if curr_pos == target_pos:
                self.fixed_tiles[tile_num] = target_pos
                continue  # Look for the next tile that is NOT at its target

            # Heuristic: Manhattan distance of tile to its target +
            # (small penalty if blank is not adjacent to the tile for easy swap)
            dist_tile_to_target = sim_manhattan_distance(curr_pos, target_pos)
            zero_pos = sim_find_zero_pos(self.puzzle_state)
            dist_blank_to_tile = sim_manhattan_distance(zero_pos, curr_pos) if zero_pos else float('inf')

            # A simple heuristic: distance of tile + 0.1 * distance of blank to tile
            # This encourages moving the blank near the tile to be placed.
            # Add a larger penalty if the tile is blocking the blank's target position
            heuristic_val = dist_tile_to_target + (dist_blank_to_tile * 0.1)

            if heuristic_val < min_dist_h:
                min_dist_h = heuristic_val
                easiest_tile_to_place = tile_num
            # Break after finding the first non-fixed, non-target tile to prioritize smaller numbers
            if easiest_tile_to_place is not None:  # Found a candidate
                break

        if easiest_tile_to_place is not None:
            self.current_target_tile_and_pos = (easiest_tile_to_place, SIM_TARGET_POSITIONS[easiest_tile_to_place])
            tile_val, (r_target, c_target) = self.current_target_tile_and_pos
            self.status_message = f"Target: Place tile {tile_val} at ({r_target},{c_target})"
        else:
            # All numbered tiles are in place, check if blank is also in place
            blank_target_pos = SIM_TARGET_POSITIONS.get(0)
            current_blank_pos = sim_find_zero_pos(self.puzzle_state)
            if current_blank_pos == blank_target_pos:
                self.all_subgoals_completed = True
                self.status_message = "COMPLETE! Puzzle Solved."
            elif current_blank_pos and blank_target_pos:  # If blank is not at target, make it the target
                self.current_target_tile_and_pos = (0, blank_target_pos)  # Target is blank (0)
                self.status_message = f"Target: Move blank to {blank_target_pos}"
            else:  # Should mean all are placed, including blank
                self.all_subgoals_completed = True
                self.status_message = "Completed or no further targets."

        if sim_check_goal_state_standard(self.puzzle_state):
            self.all_subgoals_completed = True
            self.status_message = "COMPLETE! Puzzle Solved."

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.solve_button_rect.collidepoint(
                mouse_pos) and not self.is_animating and not self.all_subgoals_completed:
            self.solve_current_subgoal()
            return True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.reset_simulation()
            return True
        return False

    def solve_current_subgoal(self):
        if self.is_animating or self.all_subgoals_completed or not self.current_target_tile_and_pos:
            if not self.current_target_tile_and_pos and not self.all_subgoals_completed:
                self.determine_next_easiest_subgoal()  # Try to find a new subgoal
            return

        tile_to_move, target_pos_for_tile = self.current_target_tile_and_pos
        current_pos_of_tile = sim_get_tile_pos(self.puzzle_state, tile_to_move)

        if current_pos_of_tile == target_pos_for_tile:
            if tile_to_move != 0:  # If it's a numbered tile
                self.fixed_tiles[tile_to_move] = target_pos_for_tile
            self.determine_next_easiest_subgoal()  # Tile already in place, find next
            return

        self.status_message = f"Finding path for tile {tile_to_move} to {target_pos_for_tile}..."
        # self.app_ref.draw() # Avoid recursive draw if called from update loop
        # pygame.display.flip()

        path_actions = a_star_solve_subgoal_sim(self.puzzle_state, tile_to_move, target_pos_for_tile, self.fixed_tiles)

        if path_actions:
            self.animation_path = path_actions
            self.current_anim_step = 0
            self.is_animating = True
            self.status_message = f"Moving tile {tile_to_move} ({len(path_actions)} steps)..."
        else:
            self.status_message = f"Error: No path found for tile {tile_to_move} to {target_pos_for_tile}!"
            # Potentially try to find another subgoal or indicate stuck
            # For now, user might need to reset or it might resolve if blank moves
            self.current_target_tile_and_pos = None  # Clear target to re-evaluate

    def update(self):
        if self.is_animating and self.animation_path:
            current_time = pygame.time.get_ticks()
            if current_time - getattr(self, '_last_anim_time', 0) >= self.animation_delay_per_step:
                self._last_anim_time = current_time
                action = self.animation_path[self.current_anim_step]
                self.puzzle_state = sim_apply_action_standard(self.puzzle_state, action)
                self.current_anim_step += 1
                if self.current_anim_step >= len(self.animation_path):
                    self.is_animating = False
                    self.animation_path = []
                    if self.current_target_tile_and_pos:
                        tile_placed, final_pos = self.current_target_tile_and_pos
                        if tile_placed != 0:  # Only fix numbered tiles this way
                            self.fixed_tiles[tile_placed] = final_pos
                    self.determine_next_easiest_subgoal()  # Determine next after animation
        elif not self.is_animating and not self.all_subgoals_completed and not self.current_target_tile_and_pos:
            self.determine_next_easiest_subgoal()  # If no target, try to find one

    def draw(self, screen, mouse_pos, is_drawing_temp_message=False):
        pygame.draw.rect(screen, SIM_CONTENT_BACKGROUND_COLOR, self.content_rect)
        self.solve_button_rect = pygame.Rect(self.content_rect.centerx - 130, self.content_rect.top + 15, 260, 45)
        btn_text = self.solve_button_text_default
        btn_bg = SIM_BUTTON_BG_COLOR
        can_click = not self.is_animating and not self.all_subgoals_completed and self.current_target_tile_and_pos

        if is_drawing_temp_message: can_click = False  # Override if temp message

        if not can_click:
            btn_bg = SIM_DISABLED_BUTTON_BG_COLOR
            if self.is_animating:
                btn_text = "Moving..."
            elif self.all_subgoals_completed:
                btn_text = "COMPLETED!"
            elif not self.current_target_tile_and_pos:  # No current target, but not yet complete
                btn_text = "Select Target..."  # Or "Determining..."
        elif self.solve_button_rect.collidepoint(mouse_pos):
            btn_bg = SIM_BUTTON_HOVER_COLOR

        pygame.draw.rect(screen, btn_bg, self.solve_button_rect, border_radius=8)
        solve_text_surf = self.button_font.render(btn_text, True, SIM_BUTTON_TEXT_COLOR)
        screen.blit(solve_text_surf, solve_text_surf.get_rect(center=self.solve_button_rect.center))

        status_surf = self.status_font.render(self.status_message, True, SIM_TEXT_COLOR_DARK)
        screen.blit(status_surf,
                    status_surf.get_rect(centerx=self.content_rect.centerx, top=self.solve_button_rect.bottom + 20))

        puzzle_x = self.content_rect.centerx - self.puzzle_visual_width // 2
        puzzle_y = status_surf.get_rect(centerx=self.content_rect.centerx,
                                        top=self.solve_button_rect.bottom + 20).bottom + 30

        if self.puzzle_state:
            draw_single_puzzle_and_or_sim(screen, self.tile_font, self.puzzle_state, self.fixed_tiles,
                                          self.current_target_tile_and_pos,  # Pass current target
                                          puzzle_x, puzzle_y, SIM_DISPLAY_TILE_SIZE_AND_OR)


class PartiallyObservableSim:
    def __init__(self, app_ref, content_rect):
        self.app_ref = app_ref
        self.content_rect = content_rect
        self.tile_font = app_ref.sim_tile_font_po
        self.status_font = app_ref.sim_status_font
        self.num_states = 9
        self.cols = 3
        self.rows = (self.num_states + self.cols - 1) // self.cols
        self.puzzle_w = SIM_GRID_SIZE * SIM_DISPLAY_TILE_SIZE_PO
        self.puzzle_h = SIM_GRID_SIZE * SIM_DISPLAY_TILE_SIZE_PO
        self.padding = 10
        self.margin = 15
        self.top_info_h = 40
        self.delay = 300
        self.reset_simulation_full()

    def reset_simulation_full(self):
        self.belief_set = sim_generate_solvable_close_states_po(self.num_states)
        self.steps = 0
        self.last_action = "None"
        self.auto_active = True
        self.timer = pygame.time.get_ticks()
        self.goal_indices = []  # Indices of belief states that reached goal
        self.status_msg = "Starting random actions... (SPACE: Pause/Resume, R: Reset)"

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_simulation_full()
                return True
            if event.key == pygame.K_SPACE:
                self.auto_active = not self.auto_active
                if self.auto_active and not self.goal_indices:  # Resume only if no goal found yet
                    self.status_msg = f"Resuming... (Step {self.steps})"
                    self.timer = pygame.time.get_ticks()  # Reset timer on resume
                elif not self.auto_active:
                    self.status_msg = f"Paused at step {self.steps}. SPACE to resume."
                elif self.goal_indices:  # If paused and goal was found
                    self.status_msg = f"Goal at {', '.join(map(str, [g + 1 for g in self.goal_indices]))}! Press 'R' to reset."
                return True
        return False

    def perform_random_step(self):
        if not self.auto_active or self.goal_indices: return  # Stop if paused or any goal found
        self.steps += 1
        action = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.last_action = action
        new_set = []
        for i, state in enumerate(self.belief_set):
            if i in self.goal_indices:  # If this state already reached goal, keep it as is
                new_set.append(copy.deepcopy(state))
                continue
            new_s = sim_apply_single_action_to_state_po(state, action)
            new_set.append(new_s)
        self.belief_set = new_set
        self.check_goal()

    def check_goal(self):
        # if not self.auto_active and self.goal_indices: return # No need to recheck if paused and goal found
        new_goals_found_this_step = False
        for i, p_state in enumerate(self.belief_set):
            if i not in self.goal_indices and sim_check_goal_state_standard(p_state):
                self.goal_indices.append(i)
                new_goals_found_this_step = True

        if new_goals_found_this_step:
            # self.auto_active = False # Pause on first goal found, or let it continue? For now, pause.
            found_str = ", ".join(str(idx + 1) for idx in self.goal_indices)
            self.status_msg = f"GOAL at matrix {found_str} after {self.steps} steps! (Last: {self.last_action})"
            if len(self.goal_indices) == self.num_states:  # All states reached goal
                self.auto_active = False
                self.status_msg = f"ALL {self.num_states} matrices reached GOAL after {self.steps} steps!"


        elif self.auto_active:  # No new goals, and still active
            self.status_msg = f"Step {self.steps} after '{self.last_action}'. SPACE: Pause/Resume."

    def update(self):
        if self.auto_active and not self.goal_indices and pygame.time.get_ticks() - self.timer >= self.delay:
            self.perform_random_step()
            self.timer = pygame.time.get_ticks()

    def draw(self, screen, mouse_pos):
        pygame.draw.rect(screen, SIM_CONTENT_BACKGROUND_COLOR, self.content_rect)
        status_s = self.status_font.render(self.status_msg, True, SIM_TEXT_COLOR_DARK)
        screen.blit(status_s, status_s.get_rect(centerx=self.content_rect.centerx, top=self.content_rect.top + 10))

        draw_y = self.content_rect.top + self.top_info_h + 5
        for i, state in enumerate(self.belief_set):
            if i >= self.num_states: break  # Should not happen if belief_set is managed correctly
            r_idx, c_idx = i // self.cols, i % self.cols
            x = self.content_rect.left + self.margin + c_idx * (self.puzzle_w + self.padding)
            y = draw_y + r_idx * (self.puzzle_h + self.padding)

            is_solved_this_state = sim_check_goal_state_standard(state)  # Check current status
            is_consistent_with_fixed = sim_check_consistent_with_goal_fixed_part_po(state)
            is_marked_as_found_goal = i in self.goal_indices

            sim_draw_belief_state_po(screen, self.tile_font, state, x, y, SIM_DISPLAY_TILE_SIZE_PO,
                                     is_solved_this_state, is_consistent_with_fixed, is_marked_as_found_goal)


class NonObservableAutoRandomSim:
    def __init__(self, app_ref, content_rect):
        self.app_ref = app_ref
        self.content_rect = content_rect
        self.tile_font = app_ref.sim_tile_font_non_obs
        self.status_font = app_ref.sim_status_font
        self.num_puzzles = 32
        self.cols = 8
        self.rows = (self.num_puzzles + self.cols - 1) // self.cols
        self.puzzle_w = SIM_GRID_SIZE * SIM_DISPLAY_TILE_SIZE_NON_OBS
        self.puzzle_h = SIM_GRID_SIZE * SIM_DISPLAY_TILE_SIZE_NON_OBS
        self.padding = 5
        self.margin = 10
        self.top_info_h = 35
        self.delay = 200
        self.reset_simulation()

    def reset_simulation(self):
        self.puzzles = sim_generate_initial_states_standard_close(self.num_puzzles, root_shuffles=20,
                                                                  variation_shuffles=5)
        self.steps = 0
        self.last_action = "None"
        self.auto_active = True
        self.timer = pygame.time.get_ticks()
        self.goal_indices = []  # Store indices of puzzles that reached the goal
        self.status_msg = "Starting auto scenario... (SPACE: Pause/Resume, R: Reset)"

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_simulation()
                return True
            if event.key == pygame.K_SPACE:
                self.auto_active = not self.auto_active
                if self.auto_active and not self.goal_indices:  # Resume only if no goal found yet
                    self.status_msg = f"Resuming... (Step {self.steps})"
                    self.timer = pygame.time.get_ticks()  # Reset timer on resume
                elif not self.auto_active:
                    self.status_msg = f"Paused at step {self.steps}. SPACE to resume."
                elif self.goal_indices:  # If paused and goal was found
                    self.status_msg = f"Goal at {len(self.goal_indices)} matrices! Press 'R' to reset."
                return True
        return False

    def perform_random_step(self):
        if not self.auto_active or len(
            self.goal_indices) == self.num_puzzles: return  # Stop if paused or all goals found
        self.steps += 1
        action = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.last_action = action

        new_goals_found_this_step = False
        for i in range(len(self.puzzles)):
            if i in self.goal_indices: continue  # Skip if already solved

            self.puzzles[i] = sim_apply_action_standard(self.puzzles[i], action)
            if sim_check_goal_state_standard(self.puzzles[i]) and i not in self.goal_indices:
                self.goal_indices.append(i)
                new_goals_found_this_step = True

        if new_goals_found_this_step:
            if len(self.goal_indices) == self.num_puzzles:  # All puzzles solved
                self.auto_active = False  # Stop auto mode
                self.status_msg = f"ALL {self.num_puzzles} puzzles SOLVED in {self.steps} steps! (Last: {self.last_action})"
            else:  # Some new goals found, but not all
                self.status_msg = f"{len(self.goal_indices)}/{self.num_puzzles} solved. Step {self.steps} after '{self.last_action}'."
        elif self.auto_active:  # No new goals, and still active
            self.status_msg = f"Step {self.steps} after '{self.last_action}'. SPACE: Pause/Resume."

    def update(self):
        if self.auto_active and len(
                self.goal_indices) < self.num_puzzles and pygame.time.get_ticks() - self.timer >= self.delay:
            self.perform_random_step()
            self.timer = pygame.time.get_ticks()

    def draw(self, screen, mouse_pos):
        pygame.draw.rect(screen, SIM_CONTENT_BACKGROUND_COLOR, self.content_rect)
        status_s = self.status_font.render(self.status_msg, True, SIM_TEXT_COLOR_DARK)
        screen.blit(status_s, status_s.get_rect(centerx=self.content_rect.centerx, top=self.content_rect.top + 10))

        draw_y = self.content_rect.top + self.top_info_h + 5
        total_grid_w = self.cols * self.puzzle_w + max(0, self.cols - 1) * self.padding
        offset_x = (self.content_rect.width - total_grid_w) // 2  # Center the grid of puzzles

        for i, p_state in enumerate(self.puzzles):
            r_idx, c_idx = i // self.cols, i % self.cols
            x = self.content_rect.left + offset_x + c_idx * (self.puzzle_w + self.padding)
            y = draw_y + r_idx * (self.puzzle_h + self.padding)

            if y + self.puzzle_h > self.content_rect.bottom - self.padding: continue  # Don't draw if off-screen

            is_found_and_goal = i in self.goal_indices  # Check if this puzzle is marked as solved
            sim_draw_single_puzzle_highlight_correct(screen, self.tile_font, p_state, SIM_STANDARD_GOAL_STATE_LIST, x,
                                                     y, SIM_DISPLAY_TILE_SIZE_NON_OBS, is_found_and_goal)


def sim_draw_belief_state_po(screen, font, state, x, y, tile_sz, is_solved_current, is_consistent_fixed,
                             is_marked_goal=False):
    base_rect = pygame.Rect(x, y, tile_sz * SIM_GRID_SIZE, tile_sz * SIM_GRID_SIZE)
    if is_marked_goal and is_solved_current:  # Highlight if it's marked and currently solved
        pygame.draw.rect(screen, SIM_HIGHLIGHT_FOUND_GOAL_BORDER, base_rect.inflate(6, 6), 3,
                         border_radius=SIM_TILE_BORDER_RADIUS + 2)

    for r, row_data in enumerate(state):
        for c, num in enumerate(row_data):
            rect = pygame.Rect(x + c * tile_sz, y + r * tile_sz, tile_sz, tile_sz)
            pygame.draw.rect(screen, SIM_TILE_EMPTY_COLOR if num == 0 else SIM_TILE_COLOR, rect,
                             border_radius=SIM_TILE_BORDER_RADIUS)

            hl_surf = pygame.Surface((tile_sz, tile_sz), pygame.SRCALPHA)
            drew_highlight = False
            if is_solved_current:  # If the current state of this matrix is the goal
                hl_surf.fill(SIM_HIGHLIGHT_SOLVED_PUZZLE)
                screen.blit(hl_surf, rect.topleft)
                drew_highlight = True
            elif is_consistent_fixed and r == 0:  # Highlight fixed top row if consistent
                # Check if the whole row is consistent, not just one tile
                if state[0] == SIM_PARTIAL_OBSERVABLE_GOAL_FIXED_PART[0]:
                    hl_surf.fill(SIM_HIGHLIGHT_YELLOW_PO_ROW)
                    screen.blit(hl_surf, rect.topleft)
                    drew_highlight = True

            if num != 0:
                text_s = font.render(str(num), True, SIM_TEXT_COLOR_ON_TILE)
                screen.blit(text_s, text_s.get_rect(center=rect.center))

            pygame.draw.rect(screen, SIM_TILE_BORDER_COLOR, rect, SIM_TILE_BORDER_WIDTH,
                             border_radius=SIM_TILE_BORDER_RADIUS)


def sim_draw_single_puzzle_highlight_correct(screen, font, p_state, goal_s_list, x, y, tile_sz, is_solved_board=False):
    base_rect = pygame.Rect(x, y, tile_sz * SIM_GRID_SIZE, tile_sz * SIM_GRID_SIZE)
    if is_solved_board:  # If this entire board is marked as solved
        pygame.draw.rect(screen, SIM_HIGHLIGHT_FOUND_GOAL_BORDER, base_rect.inflate(6, 6), 3,
                         border_radius=SIM_TILE_BORDER_RADIUS + 2)

    for r, row_data in enumerate(p_state):
        for c, num in enumerate(row_data):
            rect = pygame.Rect(x + c * tile_sz, y + r * tile_sz, tile_sz, tile_sz)
            is_correct_pos = (num != 0 and num == goal_s_list[r][c])  # Tile is in its correct final position

            pygame.draw.rect(screen, SIM_TILE_EMPTY_COLOR if num == 0 else SIM_TILE_COLOR, rect,
                             border_radius=SIM_TILE_BORDER_RADIUS)

            hl_surf = pygame.Surface((tile_sz, tile_sz), pygame.SRCALPHA)
            drew_highlight = False
            if is_solved_board and num != 0:  # If board is solved, all non-blank tiles are "solved"
                hl_surf.fill(SIM_HIGHLIGHT_SOLVED_PUZZLE)
                screen.blit(hl_surf, rect.topleft)
                drew_highlight = True
            elif is_correct_pos:  # If not solved board, but this tile is in correct pos
                hl_surf.fill(SIM_HIGHLIGHT_GREEN_CORRECT_POS)
                screen.blit(hl_surf, rect.topleft)
                drew_highlight = True

            if num != 0:
                text_s = font.render(str(num), True, SIM_TEXT_COLOR_ON_TILE)
                screen.blit(text_s, text_s.get_rect(center=rect.center))

            pygame.draw.rect(screen, SIM_TILE_BORDER_COLOR, rect, SIM_TILE_BORDER_WIDTH,
                             border_radius=SIM_TILE_BORDER_RADIUS)


def draw_single_puzzle_and_or_sim(screen, font, p_state, fixed_dict, current_target, x, y, tile_sz):
    target_tile_val, target_tile_pos = -1, (-1, -1)
    if current_target:
        target_tile_val, target_tile_pos = current_target

    for r, row_data in enumerate(p_state):
        for c, num in enumerate(row_data):
            rect = pygame.Rect(x + c * tile_sz, y + r * tile_sz, tile_sz, tile_sz)
            is_fixed_and_correct = (num != 0 and num in fixed_dict and fixed_dict[num] == (r, c))
            is_current_target_tile = (num != 0 and num == target_tile_val)
            is_target_location_for_current_target = ((r, c) == target_tile_pos and target_tile_val != -1)

            pygame.draw.rect(screen, SIM_TILE_EMPTY_COLOR if num == 0 else SIM_TILE_COLOR, rect,
                             border_radius=SIM_TILE_BORDER_RADIUS)

            # Highlight for fixed tiles
            if is_fixed_and_correct:
                hl_surf_fixed = pygame.Surface((tile_sz, tile_sz), pygame.SRCALPHA)
                hl_surf_fixed.fill(SIM_HIGHLIGHT_FIXED_TILE_BG)
                screen.blit(hl_surf_fixed, rect.topleft)

            # Highlight for the current target tile's location
            if is_target_location_for_current_target:
                pygame.draw.rect(screen, (255, 165, 0, 100), rect.inflate(-2, -2),
                                 border_radius=SIM_TILE_BORDER_RADIUS)  # Orange highlight for target location

            if num != 0:
                text_s = font.render(str(num), True, SIM_TEXT_COLOR_ON_TILE)
                text_color = SIM_TEXT_COLOR_ON_TILE
                if is_current_target_tile: text_color = (255, 0, 0)  # Highlight current target tile text red
                text_s = font.render(str(num), True, text_color)
                screen.blit(text_s, text_s.get_rect(center=rect.center))

            border_w, border_c = SIM_TILE_BORDER_WIDTH, SIM_TILE_BORDER_COLOR
            if is_fixed_and_correct:
                border_w = 2
                border_c = SIM_HIGHLIGHT_AND_OR_FIXED_BORDER
            elif is_current_target_tile:  # Special border for the tile that is the current target
                border_w = 2
                border_c = (255, 0, 0)  # Red border for target tile

            pygame.draw.rect(screen, border_c, rect, border_w, border_radius=SIM_TILE_BORDER_RADIUS)


def a_star_solve_subgoal_sim(initial_list, tile_to_place, target_pos_for_tile, fixed_tiles_dict):
    initial_tuple = tuple(map(tuple, initial_list))
    current_pos_of_tile = sim_get_tile_pos(initial_tuple, tile_to_place)

    if current_pos_of_tile == target_pos_for_tile:
        return []  # Already at target

    # If the tile to place is the blank tile (0)
    if tile_to_place == 0:
        # Goal is to move the blank to target_pos_for_tile
        # Heuristic: Manhattan distance of blank to its target
        # Cost: Number of moves
        # No need to worry about 'fixed_tiles_dict' for moving the blank itself,
        # as fixed_tiles_dict refers to numbered tiles.
        # However, the blank cannot move INTO a space occupied by a tile that is
        # intended to be fixed *if that fixed tile is not the one being swapped with*.
        # This is implicitly handled by the successor generation: blank swaps with a tile.
        # If that tile is fixed, the move is disallowed by the check below.
        pass  # Standard A* logic applies, heuristic below will be distance of blank.

    entry_count = 0  # Tie-breaker for heapq
    # Heuristic: Manhattan distance of 'tile_to_place' to 'target_pos_for_tile'
    # If tile_to_place is 0 (blank), it's dist of blank to its target.
    # If tile_to_place is a number, it's dist of that number to its target.
    h_initial = sim_manhattan_distance(current_pos_of_tile, target_pos_for_tile)

    # If tile_to_place is NOT blank, we also need to consider moving the blank tile
    # to a position adjacent to 'tile_to_place' to enable moving it,
    # and then moving 'tile_to_place' into the blank's old spot.
    # A more complex heuristic could be:
    #   dist(tile, target_tile_pos) + dist(blank, current_pos_of_tile)
    # For now, simple Manhattan distance of the tile itself.

    open_set = [(h_initial, 0, entry_count, initial_tuple, [])]  # (f_cost, g_cost, tie_breaker, state, path_actions)
    heapq.heapify(open_set)
    # closed_set stores g_cost to reach a state: {state_tuple: g_cost}
    closed_set = {initial_tuple: 0}
    nodes_expanded = 0
    max_nodes_to_expand = 30000  # Safety limit

    while open_set and nodes_expanded < max_nodes_to_expand:
        _f, g_cost, _ec, current_state_tuple, path_actions_list = heapq.heappop(open_set)
        nodes_expanded += 1

        current_pos_of_tile_in_state = sim_get_tile_pos(current_state_tuple, tile_to_place)
        if current_pos_of_tile_in_state == target_pos_for_tile:
            return path_actions_list  # Goal reached for this subgoal

        # Generate successors by moving the blank tile
        zero_r, zero_c = sim_find_zero_pos(current_state_tuple)
        current_state_list_form = [list(r) for r in current_state_tuple]

        for dr_move, dc_move, action_name in [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]:
            next_zero_r, next_zero_c = zero_r + dr_move, zero_c + dc_move

            if 0 <= next_zero_r < SIM_GRID_SIZE and 0 <= next_zero_c < SIM_GRID_SIZE:
                # Tile that the blank is about to swap with
                tile_being_swapped_val = current_state_list_form[next_zero_r][next_zero_c]

                # Constraint: Cannot move a tile that is already fixed in its position,
                # UNLESS that tile is the 'tile_to_place' and we are moving it.
                # OR if the tile_being_swapped is the blank itself (which is tile_to_place == 0)
                if tile_to_place != 0 and \
                        tile_being_swapped_val in fixed_tiles_dict and \
                        fixed_tiles_dict[tile_being_swapped_val] == (next_zero_r, next_zero_c) and \
                        tile_being_swapped_val != tile_to_place:  # If it's fixed and NOT the one we are trying to move
                    continue

                new_state_list_form = copy.deepcopy(current_state_list_form)
                # Perform the swap (blank moves)
                new_state_list_form[zero_r][zero_c], new_state_list_form[next_zero_r][next_zero_c] = \
                    new_state_list_form[next_zero_r][next_zero_c], new_state_list_form[zero_r][zero_c]

                next_state_tuple = tuple(map(tuple, new_state_list_form))
                new_g_cost = g_cost + 1

                if next_state_tuple in closed_set and closed_set[next_state_tuple] <= new_g_cost:
                    continue  # Already found a shorter or equal path to this state

                closed_set[next_state_tuple] = new_g_cost

                # Heuristic for the next state
                pos_of_tile_in_next_state = sim_get_tile_pos(next_state_tuple, tile_to_place)
                if not pos_of_tile_in_next_state: continue  # Should not happen

                h_cost_next = sim_manhattan_distance(pos_of_tile_in_next_state, target_pos_for_tile)

                # Additional heuristic: if we are not moving the blank (tile_to_place != 0),
                # add a small penalty for the blank not being adjacent to the target tile's *current* position.
                # This is to encourage the blank to move towards the tile we want to place.
                if tile_to_place != 0:
                    current_blank_pos_in_next = sim_find_zero_pos(next_state_tuple)
                    if sim_manhattan_distance(current_blank_pos_in_next, pos_of_tile_in_next_state) > 1:
                        h_cost_next += 0.5  # Small penalty

                new_f_cost = new_g_cost + h_cost_next
                entry_count += 1
                heapq.heappush(open_set, (
                new_f_cost, new_g_cost, entry_count, next_state_tuple, path_actions_list + [action_name]))
    return None  # No path found within limits


if __name__ == "__main__":
    app = EightPuzzleApp()
    try:
        if platform.system() == "Emscripten":
            # For web environment (e.g., Pyodide, Brython)
            # asyncio.run might not be the standard way to run the main loop.
            # ensure_future is often used, or a specific runner for the web framework.
            asyncio.ensure_future(app.main_loop())
            # If using Pygbag, it might have its own way to start the asyncio loop.
            # For simple Pygame web, you might not even use asyncio directly in main.
        else:
            # For standard desktop Python
            asyncio.run(app.main_loop())
    except KeyboardInterrupt:
        print("Application stopped by user (KeyboardInterrupt).")
        app.app_should_quit = True  # Ensure flag is set for graceful shutdown
    except SystemExit:
        print("Application exited (SystemExit).")
        # app.app_should_quit might already be true or irrelevant here
    finally:
        print("Cleaning up...")
        pygame.quit()
        # Attempt to destroy Tkinter root if it exists
        if hasattr(app, 'root') and app.root:
            try:
                if app.root.winfo_exists():  # Check if window exists before destroying
                    app.root.destroy()
                    print("Tkinter root destroyed.")
            except Exception as e:
                print(f"Error destroying Tkinter root: {e}")
        print("Application finished.")
