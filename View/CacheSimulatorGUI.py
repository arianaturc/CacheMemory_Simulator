import os
import pygame
import sys
from Controller.CacheController import CacheController
from Model.MainMemory import MainMemory


class CacheSimulatorGUI:

    def __init__(self):
        enable_high_dpi()
        pygame.init()

        self.base_width = 1500
        self.base_height = 900

        try:
            import ctypes
            dpi_scale = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0
        except Exception:
            dpi_scale = 1.0

        display_info = pygame.display.Info()
        screen_w, screen_h = display_info.current_w, display_info.current_h

        fit_scale_w = screen_w * 0.9 / self.base_width
        fit_scale_h = screen_h * 0.9 / self.base_height

        self.scale = max(1.0, min(dpi_scale, fit_scale_w, fit_scale_h))

        def sx(v): return int(v * self.scale)
        def sy(v): return int(v * self.scale)
        self.sx = sx
        self.sy = sy

        self.WIDTH = self.sx(self.base_width)
        self.HEIGHT = self.sy(self.base_height)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Cache Memory Simulator")

        self.COFFEE_BEAN = (36, 23, 21)       # #241715  (main dark background)
        self.DEEP_MOCHA = (64, 42, 44)        # #402A2C  (panels, bars, UI blocks)
        self.MAUVE_SHADOW = (112, 61, 87)     # #703D57  (buttons, accents)
        self.DUSTY_MAUVE = (149, 113, 134)    # #957186  (highlight, text accents)
        self.PASTEL_PETAL = (217, 184, 196)   # #D9B8C4  (selected button fill)

        self.WHITE = (255, 255, 255)
        self.LIGHT_TEXT = (230, 220, 220)

        self.GREEN = (60, 179, 113)
        self.RED = (220, 20, 60)

        self.font = pygame.font.Font(None, int(28 * self.scale))
        self.small_font = pygame.font.Font(None, int(22 * self.scale))
        self.tiny_font = pygame.font.Font(None, int(18 * self.scale))
        self.title_font = pygame.font.Font(None, int(36 * self.scale))
        self.header_font = pygame.font.Font(None, int(30 * self.scale))

        self.input_cache_size = "256"
        self.input_block_size = "64"
        self.main_memory_size = 65536

        self.mapping_type = "Direct"
        self.replacement_policy = "LRU"
        self.write_policy = "WriteBack"
        self.input_associativity = "2"

        self.input_address = ""
        self.input_data = ""
        self.active_input = None

        self.message = ""
        self.message_color = self.WHITE
        self.message_timer = 0

        self.view_mode = "cache"

        self.memory_scroll = 0
        self.cache_scroll = 0

        self.main_memory = MainMemory(self.main_memory_size)
        self.main_memory.write(0, f"DATA_{0}")
        for i in range(0, 2000, 64):
            self.main_memory.write(i, f"DATA_{i}")

        self.buttons = self.create_buttons()
        self.create_controller()



    def safe_int(self, value, default):
        try:
            result = int(value)
            return result if result > 0 else default
        except:
            return default

    def create_controller(self):
        try:
            cache_size = self.safe_int(self.input_cache_size, 256)
            block_size = self.safe_int(self.input_block_size, 64)

            if self.mapping_type == "SetAssoc":
                associativity = self.safe_int(self.input_associativity, 2)
            else:
                associativity = 1

            self.controller = CacheController(
                cache_size,
                block_size,
                self.mapping_type,
                self.replacement_policy,
                self.write_policy,
                self.main_memory,
                associativity
            )

            self.cache_scroll = 0
            self.memory_scroll = 0

            self.message = "✓ Settings applied"
            self.message_color = self.GREEN
            self.message_timer = 180

        except Exception as e:
            self.message = f"✗ Error: {str(e)}"
            self.message_color = self.RED
            self.message_timer = 180

    # ---------------------- BUTTON CREATION --------------------------
    def create_buttons(self):
        buttons = {}

        buttons['apply'] = pygame.Rect(
            self.sx(150), self.sy(200),
            self.sx(200), self.sy(40)
        )

        buttons['view_cache'] = pygame.Rect(self.sx(520), self.sy(15), self.sx(150), self.sy(40))
        buttons['view_memory'] = pygame.Rect(self.sx(690), self.sy(15), self.sx(150), self.sy(40))
        buttons['view_stats'] = pygame.Rect(self.sx(860), self.sy(15), self.sx(150), self.sy(40))

        buttons['direct'] = pygame.Rect(self.sx(30), self.sy(300), self.sx(130), self.sy(40))
        buttons['set'] = pygame.Rect(self.sx(175), self.sy(300), self.sx(130), self.sy(40))
        buttons['full'] = pygame.Rect(self.sx(320), self.sy(300), self.sx(150), self.sy(40))

        buttons['lru'] = pygame.Rect(self.sx(30), self.sy(380), self.sx(110), self.sy(40))
        buttons['fifo'] = pygame.Rect(self.sx(155), self.sy(380), self.sx(110), self.sy(40))
        buttons['random'] = pygame.Rect(self.sx(280), self.sy(380), self.sx(110), self.sy(40))

        buttons['wb'] = pygame.Rect(self.sx(30), self.sy(480), self.sx(180), self.sy(40))
        buttons['wt'] = pygame.Rect(self.sx(225), self.sy(480), self.sx(180), self.sy(40))

        buttons['read'] = pygame.Rect(self.sx(30), self.sy(600), self.sx(130), self.sy(45))
        buttons['write'] = pygame.Rect(self.sx(180), self.sy(600), self.sx(130), self.sy(45))
        buttons['reset'] = pygame.Rect(self.sx(330), self.sy(600), self.sx(130), self.sy(45))

        return buttons

    # ---------------------- DRAW BUTTON -------------------------
    def draw_button(self, rect, text, selected=False, bg_color=None):

        if bg_color is None:
            bg_color = self.MAUVE_SHADOW

        if selected:
            color = self.PASTEL_PETAL
            text_color = self.COFFEE_BEAN
        else:
            color = bg_color
            text_color = self.WHITE

        pygame.draw.rect(self.screen, color, rect, border_radius=int(8 * self.scale))
        pygame.draw.rect(self.screen, self.PASTEL_PETAL, rect, int(2 * self.scale), border_radius=int(8 * self.scale))

        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    # ---------------------- DRAW INPUT BOX -------------------------
    def draw_input_box(self, x, y, w, h, label, value, active):
        x, y, w, h = self.sx(x), self.sy(y), self.sx(w), self.sy(h)

        label_surf = self.small_font.render(label, True, self.PASTEL_PETAL)
        self.screen.blit(label_surf, (x, y - self.sy(25)))

        box = pygame.Rect(x, y, w, h)
        pygame.draw.rect(self.screen, self.DEEP_MOCHA, box)

        border_color = self.PASTEL_PETAL if active else self.DUSTY_MAUVE
        pygame.draw.rect(self.screen, border_color, box, int(3 * self.scale), border_radius=int(5 * self.scale))

        txt = self.font.render(value, True, self.WHITE)
        self.screen.blit(txt, (box.x + self.sx(8), box.y + self.sy(8)))

        return box

    # ---------------------- DRAW CACHE VIEW -------------------------
    def draw_cache_view(self):
        start_x = self.sx(540)
        start_y = self.sy(175)
        item_height = self.sy(35)
        padding = self.sx(10)

        title = self.header_font.render("Cache Memory State", True, self.PASTEL_PETAL)
        self.screen.blit(title, (start_x, self.sy(80)))

        info = f"Mapping: {self.mapping_type} | Replacement: {self.replacement_policy} | Write: {self.write_policy}"
        info_surf = self.small_font.render(info, True, self.DUSTY_MAUVE)
        self.screen.blit(info_surf, (start_x, self.sy(110)))

        header_rect = pygame.Rect(start_x, self.sy(140), self.sx(820), self.sy(30))
        pygame.draw.rect(self.screen, self.MAUVE_SHADOW, header_rect, border_radius=int(5 * self.scale))

        x_offset = start_x + padding
        headers = ["Line"]
        if self.mapping_type == "SetAssoc":
            headers.append("Set")
        headers += ["Valid", "Tag", "Dirty", "Data"]

        for h in headers:
            surf = self.small_font.render(h, True, self.WHITE)
            self.screen.blit(surf, (x_offset, self.sy(146)))
            x_offset += self.sx(90)

        lines = self.controller.cache_memory.lines
        y = start_y

        for idx, line in enumerate(lines):
            row_rect = pygame.Rect(start_x, y, self.sx(820), item_height)

            bg = self.DEEP_MOCHA if line.valid else self.COFFEE_BEAN
            pygame.draw.rect(self.screen, bg, row_rect, border_radius=int(5 * self.scale))
            pygame.draw.rect(self.screen, self.MAUVE_SHADOW, row_rect, int(1 * self.scale), border_radius=int(5 * self.scale))

            x_offset = start_x + padding
            self.screen.blit(self.small_font.render(str(idx), True, self.PASTEL_PETAL), (x_offset, y + self.sy(8)))
            x_offset += self.sx(90)

            if self.mapping_type == "SetAssoc":
                assoc = self.safe_int(self.input_associativity, 2)
                set_id = idx // assoc
                self.screen.blit(self.small_font.render(str(set_id), True, self.DUSTY_MAUVE), (x_offset, y + self.sy(8)))
                x_offset += self.sx(90)

            if line.valid:
                self.screen.blit(self.small_font.render("1", True, self.GREEN), (x_offset, y + self.sy(8)))
                x_offset += self.sx(90)

                self.screen.blit(self.small_font.render(f"0x{line.tag:04X}", True, self.WHITE), (x_offset, y + self.sy(8)))
                x_offset += self.sx(120)

                dirty_color = self.RED if line.dirtyBit else self.GREEN
                self.screen.blit(self.small_font.render("1" if line.dirtyBit else "0", True, dirty_color),
                                 (x_offset, y + self.sy(8)))
                x_offset += self.sx(90)

                data = str(line.data)
                if len(data) > 30:
                    data = data[:30] + "..."
                self.screen.blit(self.small_font.render(data, True, self.DUSTY_MAUVE), (x_offset, y + self.sy(8)))

            y += item_height + self.sy(3)

    # ---------------------- DRAW MEMORY VIEW -------------------------
    def draw_memory_view(self):
        start_x = self.sx(540)
        start_y = self.sy(140)
        item_height = self.sy(32)

        title = self.header_font.render("Main Memory Contents", True, self.PASTEL_PETAL)
        self.screen.blit(title, (start_x, self.sy(80)))

        sorted_addrs = sorted(self.main_memory.memory.keys())
        max_count = 20
        start_idx = min(self.memory_scroll, max(0, len(sorted_addrs) - max_count))
        end_idx = min(start_idx + max_count, len(sorted_addrs))

        y = start_y
        for i in range(start_idx, end_idx):
            addr = sorted_addrs[i]
            data = self.main_memory.memory[addr]

            row = pygame.Rect(start_x, y, self.sx(820), item_height)
            bg = self.DEEP_MOCHA if i % 2 == 0 else self.COFFEE_BEAN
            pygame.draw.rect(self.screen, bg, row, border_radius=int(5 * self.scale))
            pygame.draw.rect(self.screen, self.MAUVE_SHADOW, row, int(1 * self.scale), border_radius=int(5 * self.scale))

            text = self.small_font.render(f"0x{addr:04X}  ({addr})", True, self.WHITE)
            self.screen.blit(text, (start_x + self.sx(15), y + self.sy(6)))

            data_str = str(data)
            if len(data_str) > 35:
                data_str = data_str[:35] + "..."
            data_surf = self.small_font.render(f"→ {data_str}", True, self.DUSTY_MAUVE)
            self.screen.blit(data_surf, (start_x + self.sx(280), y + self.sy(6)))

            y += item_height + self.sy(2)

    # ---------------------- DRAW STATISTICS -------------------------
    def draw_statistics_view(self):
        start_x = self.sx(600)
        start_y = self.sy(160)

        title = self.header_font.render("Cache Performance Statistics", True, self.PASTEL_PETAL)
        self.screen.blit(title, (start_x, self.sy(80)))

        stats = self.controller.statistics
        total = stats.hits + stats.misses
        hit_rate = (stats.hits / total * 100) if total > 0 else 0
        miss_rate = 100 - hit_rate

        items = [
            ("Total Accesses", str(total), self.DUSTY_MAUVE),
            ("Cache Hits", str(stats.hits), self.GREEN),
            ("Cache Misses", str(stats.misses), self.RED),
            ("Hit Rate", f"{hit_rate:.2f}%", self.GREEN),
            ("Miss Rate", f"{miss_rate:.2f}%", self.RED),
        ]

        y = start_y
        for label, value, col in items:
            box = pygame.Rect(start_x, y, self.sx(600), self.sy(55))
            pygame.draw.rect(self.screen, self.DEEP_MOCHA, box, border_radius=int(8 * self.scale))
            pygame.draw.rect(self.screen, col, box, int(2 * self.scale), border_radius=int(8 * self.scale))

            label_surf = self.font.render(label + ":", True, self.WHITE)
            self.screen.blit(label_surf, (start_x + self.sx(20), y + self.sy(15)))

            value_surf = self.title_font.render(value, True, col)
            val_rect = value_surf.get_rect(right=start_x + self.sx(580), centery=y + self.sy(27))
            self.screen.blit(value_surf, val_rect)

            y += self.sy(70)

    # --------------------------- MAIN DRAW -----------------------------
    def draw(self):

        self.screen.fill(self.COFFEE_BEAN)

        left_panel_width = self.sx(500)
        nav_bar = pygame.Rect(left_panel_width, 0, self.WIDTH - left_panel_width, self.sy(70))
        pygame.draw.rect(self.screen, self.DEEP_MOCHA, nav_bar)
        pygame.draw.line(self.screen, self.MAUVE_SHADOW,
                         (left_panel_width, self.sy(70)),
                         (self.WIDTH, self.sy(70)),
                         int(2 * self.scale))

        self.draw_button(self.buttons['view_cache'], "CACHE", self.view_mode == "cache")
        self.draw_button(self.buttons['view_memory'], "MEMORY", self.view_mode == "memory")
        self.draw_button(self.buttons['view_stats'], "STATISTICS", self.view_mode == "statistics")

        if self.view_mode == "cache":
            self.draw_cache_view()
        elif self.view_mode == "memory":
            self.draw_memory_view()
        else:
            self.draw_statistics_view()

        self.draw_left_panel()

        if self.message_timer > 0:
            self.message_timer -= 1

        pygame.display.flip()

    # --------------------------- LEFT PANEL -----------------------------
    def draw_left_panel(self):
        panel_width = self.sx(500)
        panel = pygame.Rect(0, 0, panel_width, self.HEIGHT)
        pygame.draw.rect(self.screen, self.DEEP_MOCHA, panel)
        pygame.draw.line(self.screen, self.MAUVE_SHADOW,
                         (panel_width, 0),
                         (panel_width, self.HEIGHT),
                         int(3 * self.scale))

        title = self.title_font.render("Control Panel", True, self.PASTEL_PETAL)
        self.screen.blit(title, (self.sx(160), self.sy(30)))

        config_label = self.font.render("Cache Configuration", True, self.PASTEL_PETAL)
        self.screen.blit(config_label, (self.sx(30), self.sy(70)))

        self.cache_size_box = self.draw_input_box(30, 125, 200, 40,
                                                  "Cache Size (bytes)",
                                                  self.input_cache_size,
                                                  self.active_input == "cache")

        self.block_size_box = self.draw_input_box(250, 125, 200, 40,
                                                  "Block Size (bytes)",
                                                  self.input_block_size,
                                                  self.active_input == "block")

        self.draw_button(self.buttons['apply'], "APPLY SETTINGS", False, self.MAUVE_SHADOW)

        mapping_label = self.font.render("Mapping Strategy", True, self.PASTEL_PETAL)
        self.screen.blit(mapping_label, (self.sx(30), self.sy(270)))

        self.draw_button(self.buttons['direct'], "Direct", self.mapping_type == "Direct")
        self.draw_button(self.buttons['set'], "Set-Assoc", self.mapping_type == "SetAssoc")
        self.draw_button(self.buttons['full'], "Fully-Assoc", self.mapping_type == "FullyAssoc")

        current_y = 370

        if self.mapping_type == "SetAssoc":
            self.associativity_box = self.draw_input_box(
                130, current_y, 220, 35,
                "Associativity (lines/set)",
                self.input_associativity,
                self.active_input == "associativity"
            )
            current_y += 70

        repl_label = self.font.render("Replacement Policy", True, self.PASTEL_PETAL)
        self.screen.blit(repl_label, (self.sx(30), self.sy(current_y + 30)))

        self.buttons['lru'].y = self.sy(current_y + 60)
        self.buttons['fifo'].y = self.sy(current_y + 60)
        self.buttons['random'].y = self.sy(current_y + 60)

        self.draw_button(self.buttons['lru'], "LRU", self.replacement_policy == "LRU")
        self.draw_button(self.buttons['fifo'], "FIFO", self.replacement_policy == "FIFO")
        self.draw_button(self.buttons['random'], "Random", self.replacement_policy == "Random")

        current_y += 100

        write_label = self.font.render("Write Policy", True, self.PASTEL_PETAL)
        self.screen.blit(write_label, (self.sx(30), self.sy(current_y + 20)))

        self.buttons['wb'].y = self.sy(current_y + 50)
        self.buttons['wt'].y = self.sy(current_y + 50)

        self.draw_button(self.buttons['wb'], "Write-Back", self.write_policy == "WriteBack")
        self.draw_button(self.buttons['wt'], "Write-Through", self.write_policy == "WriteThrough")

        current_y += 100

        ops_label = self.font.render("Operations", True, self.PASTEL_PETAL)
        self.screen.blit(ops_label, (self.sx(30), self.sy(current_y + 10)))

        self.buttons['read'].y = self.sy(current_y + 30)
        self.buttons['write'].y = self.sy(current_y + 30)
        self.buttons['reset'].y = self.sy(current_y + 30)

        self.draw_button(self.buttons['read'], "READ", False, self.GREEN)
        self.draw_button(self.buttons['write'], "WRITE", False, self.RED)
        self.draw_button(self.buttons['reset'], "RESET", False, self.MAUVE_SHADOW)

        current_y += 120

        self.address_box = self.draw_input_box(30, current_y, 200, 40,
                                               "Address (decimal)",
                                               self.input_address,
                                               self.active_input == "address")

        self.data_box = self.draw_input_box(250, current_y, 200, 40,
                                            "Data",
                                            self.input_data,
                                            self.active_input == "data")

        if self.message and self.message_timer > 0:
            msg_y = current_y + 60
            msg_bg = pygame.Rect(self.sx(20), self.sy(msg_y),
                                 self.sx(460), self.sy(50))
            pygame.draw.rect(self.screen, self.DEEP_MOCHA, msg_bg, border_radius=int(8 * self.scale))
            pygame.draw.rect(self.screen, self.message_color, msg_bg, int(3 * self.scale), border_radius=int(8 * self.scale))

            msg_surf = self.small_font.render(self.message, True, self.message_color)
            msg_rect = msg_surf.get_rect(center=msg_bg.center)
            self.screen.blit(msg_surf, msg_rect)

    # ---------------------------- CLICK HANDLER -----------------------------
    def handle_click(self, pos):

        if self.buttons['view_cache'].collidepoint(pos):
            self.view_mode = "cache"
            return
        elif self.buttons['view_memory'].collidepoint(pos):
            self.view_mode = "memory"
            return
        elif self.buttons['view_stats'].collidepoint(pos):
            self.view_mode = "statistics"
            return

        if self.buttons['apply'].collidepoint(pos):
            self.create_controller()
            return

        if self.cache_size_box.collidepoint(pos):
            self.active_input = "cache"
        elif self.block_size_box.collidepoint(pos):
            self.active_input = "block"
        elif self.mapping_type == "SetAssoc" and hasattr(self, 'associativity_box') and self.associativity_box.collidepoint(pos):
            self.active_input = "associativity"
        elif self.address_box.collidepoint(pos):
            self.active_input = "address"
        elif self.data_box.collidepoint(pos):
            self.active_input = "data"
        else:
            self.active_input = None

        if self.buttons['direct'].collidepoint(pos):
            self.mapping_type = "Direct"
        elif self.buttons['set'].collidepoint(pos):
            self.mapping_type = "SetAssoc"
        elif self.buttons['full'].collidepoint(pos):
            self.mapping_type = "FullyAssoc"

        if self.buttons['lru'].collidepoint(pos):
            self.replacement_policy = "LRU"
        elif self.buttons['fifo'].collidepoint(pos):
            self.replacement_policy = "FIFO"
        elif self.buttons['random'].collidepoint(pos):
            self.replacement_policy = "Random"

        if self.buttons['wb'].collidepoint(pos):
            self.write_policy = "WriteBack"
        elif self.buttons['wt'].collidepoint(pos):
            self.write_policy = "WriteThrough"

        if self.buttons['read'].collidepoint(pos):
            if self.input_address.isdigit():
                try:
                    data = self.controller.read(int(self.input_address))
                    self.message = f"✓ READ: {data}"
                    self.message_color = self.GREEN
                    self.message_timer = 180
                except Exception as e:
                    self.message = f"✗ Error: {str(e)}"
                    self.message_color = self.RED
                    self.message_timer = 180
            else:
                self.message = "✗ Invalid address"
                self.message_color = self.RED
                self.message_timer = 180

        elif self.buttons['write'].collidepoint(pos):
            if self.input_address.isdigit():
                try:
                    data = self.input_data if self.input_data else f"Data_{self.input_address}"
                    self.controller.write(int(self.input_address), data)
                    self.message = "✓ WRITE successful"
                    self.message_color = self.GREEN
                    self.message_timer = 180
                except Exception as e:
                    self.message = f"✗ Error: {str(e)}"
                    self.message_color = self.RED
                    self.message_timer = 180
            else:
                self.message = "✗ Invalid address"
                self.message_color = self.RED
                self.message_timer = 180

        elif self.buttons['reset'].collidepoint(pos):
            self.main_memory = MainMemory(self.main_memory_size)
            for i in range(0, 2000, 64):
                self.main_memory.write(i, f"DATA_{i}")
            self.create_controller()

    # ---------------------------- KEY HANDLER -----------------------------
    def handle_key(self, event):
        if self.active_input is None:
            return

        if event.key == pygame.K_BACKSPACE:
            if self.active_input == "cache":
                self.input_cache_size = self.input_cache_size[:-1]
            elif self.active_input == "block":
                self.input_block_size = self.input_block_size[:-1]
            elif self.active_input == "associativity":
                self.input_associativity = self.input_associativity[:-1]
            elif self.active_input == "address":
                self.input_address = self.input_address[:-1]
            elif self.active_input == "data":
                self.input_data = self.input_data[:-1]

        elif event.key == pygame.K_RETURN:
            self.active_input = None

        else:
            if event.unicode.isdigit() or event.unicode.isalpha():
                if self.active_input == "cache":
                    self.input_cache_size += event.unicode
                elif self.active_input == "block":
                    self.input_block_size += event.unicode
                elif self.active_input == "associativity":
                    self.input_associativity += event.unicode
                elif self.active_input == "address":
                    self.input_address += event.unicode
                elif self.active_input == "data":
                    self.input_data += event.unicode

    # --------------------------- MAIN LOOP -------------------------------
    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)
                    elif event.button == 4:
                        self.memory_scroll = max(0, self.memory_scroll - 1)
                    elif event.button == 5:
                        self.memory_scroll += 1

                if event.type == pygame.KEYDOWN:
                    self.handle_key(event)

            self.draw()
            clock.tick(60)

        pygame.quit()
        sys.exit()



def enable_high_dpi(scale=3):
    os.environ["SDL_VIDEO_ALLOW_HIGHDPI"] = "1"
    try:
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass



