import pygame
import math
import sys
import random
import asyncio

pygame.init()

WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ChemSandbox - Web Optimized 3D Engine")
clock = pygame.time.Clock()

# Zabudovane fonty pro bezpecny chod na webu a tabletech
font_tiny = pygame.font.Font(None, 16)
font_small = pygame.font.Font(None, 20)
font_medium = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 34)
font_element = pygame.font.Font(None, 28)
font_alert = pygame.font.Font(None, 30)

# Vylepsena paleta barev
BG_COLOR_CENTER = (30, 35, 45)
BG_COLOR_EDGE = (10, 12, 15)
GRID_COLOR = (45, 50, 60)
UI_BG = (25, 30, 40)
UI_HOVER = (50, 60, 75)
UI_ACTIVE = (80, 130, 255)
TEXT_COLOR = (240, 240, 240)
WHITE = (255, 255, 255)
BOND_COLOR = (150, 160, 170)
ELECTRON_COLOR = (255, 255, 100)
ORBITAL_COLOR = (80, 150, 255, 40)
ALERT_COLOR = (255, 80, 80)

ELEMENTS = {
    'H':  ((255, 255, 255), 1, 1.0,   'Vodik',     1, 2.20),
    'He': ((200, 255, 255), 2, 4.0,   'Helium',    0, 0.00),
    'Li': ((200, 100, 255), 1, 6.9,   'Lithium',   1, 0.98),
    'Be': ((150, 255, 150), 2, 9.0,   'Beryllium', 2, 1.57),
    'B':  ((255, 200, 150), 3, 10.8,  'Bor',       3, 2.04),
    'C':  ((100, 100, 100), 4, 12.0,  'Uhlik',     4, 2.55),
    'N':  ((100, 150, 255), 5, 14.0,  'Dusik',     4, 3.04),
    'O':  ((255, 80, 80),   6, 16.0,  'Kyslik',    3, 3.44),
    'F':  ((150, 255, 150), 7, 19.0,  'Fluor',     1, 3.98),
    'Ne': ((200, 255, 255), 8, 20.1,  'Neon',      0, 0.00),
    'Na': ((150, 100, 255), 1, 23.0,  'Sodik',     1, 0.93),
    'Mg': ((100, 200, 100), 2, 24.3,  'Horcik',    2, 1.31),
    'Al': ((200, 200, 200), 3, 27.0,  'Hlinik',    4, 1.61),
    'Si': ((150, 150, 150), 4, 28.1,  'Kremik',    4, 1.90),
    'P':  ((255, 150, 50),  5, 31.0,  'Fosfor',    5, 2.19),
    'S':  ((255, 255, 50),  6, 32.1,  'Sira',      6, 2.58),
    'Cl': ((100, 255, 100), 7, 35.4,  'Chlor',     7, 3.16),
    'Ar': ((200, 255, 255), 8, 39.9,  'Argon',     0, 0.00),
    'K':  ((180, 120, 255), 1, 39.1,  'Draslik',   1, 0.82),
    'Ca': ((120, 220, 120), 2, 40.1,  'Vapnik',    2, 1.00),
    'Ti': ((180, 180, 190), 4, 47.8,  'Titan',     6, 1.54),
    'Fe': ((200, 100, 50),  8, 55.8,  'Zelezo',    6, 1.83),
    'Co': ((170, 150, 200), 9, 58.9,  'Kobalt',    6, 1.88),
    'Ni': ((150, 200, 150), 10, 58.6, 'Nikl',      4, 1.91),
    'Cu': ((255, 150, 100), 11, 63.5, 'Med',       4, 1.90),
    'Zn': ((180, 180, 200), 2, 65.4,  'Zinek',     4, 1.65),
    'Br': ((150, 50, 50),   7, 79.9,  'Brom',      7, 2.96),
    'Kr': ((200, 255, 255), 8, 83.7,  'Krypton',   0, 0.00),
    'Ag': ((220, 220, 220), 1, 107.8, 'Stribro',   2, 1.93),
    'I':  ((100, 50, 150),  7, 126.9, 'Jod',       7, 2.66),
    'Xe': ((200, 255, 255), 8, 131.2, 'Xenon',     0, 0.00),
    'Pt': ((210, 210, 220), 10, 195.0,'Platina',   6, 2.28),
    'Au': ((255, 215, 0),   11, 196.9,'Zlato',     4, 2.54),
    'Hg': ((180, 180, 180), 2, 200.5, 'Rtut',      2, 2.00),
    'Pb': ((100, 100, 120), 4, 207.2, 'Olovo',     4, 2.33),
    'U':  ((100, 255, 100), 6, 238.0, 'Uran',      6, 1.38)
}

TOOL_CURSOR = 0
TOOL_PAN = 1
TOOL_ADD_ATOM = 2
TOOL_ADD_BOND = 3

MODE_2D = 0
MODE_3D = 1

def generate_vignette_bg(width, height):
    """Vygeneruje moderni prechodove pozadi jednou pri startu"""
    bg = pygame.Surface((width, height))
    cx, cy = width // 2, height // 2
    max_dist = math.hypot(cx, cy)
    
    for y in range(height):
        for x in range(width):
            dist = math.hypot(x - cx, y - cy)
            ratio = min(1.0, dist / max_dist)
            
            r = int(BG_COLOR_CENTER[0] * (1 - ratio) + BG_COLOR_EDGE[0] * ratio)
            g = int(BG_COLOR_CENTER[1] * (1 - ratio) + BG_COLOR_EDGE[1] * ratio)
            b = int(BG_COLOR_CENTER[2] * (1 - ratio) + BG_COLOR_EDGE[2] * ratio)
            
            bg.set_at((x, y), (r, g, b))
    return bg

def get_bond_order(b_type):
    if b_type == 2: return 2
    if b_type == 3: return 3
    return 1

def get_en_color(en):
    if en == 0: return (150, 150, 150)
    if en < 2.4:
        t = max(0.0, (en - 0.8) / 1.6)
        return (int(50 + 205*t), int(50 + 205*t), int(255 - 205*t))
    else:
        t = min(1.0, (en - 2.4) / 1.6)
        return (255, int(255 - 205*t), 50)

def point_line_distance(px, py, x1, y1, x2, y2):
    l2 = (x1 - x2)**2 + (y1 - y2)**2
    if l2 == 0: return math.hypot(px - x1, py - y1)
    t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / l2))
    proj_x = x1 + t * (x2 - x1)
    proj_y = y1 + t * (y2 - y1)
    return math.hypot(px - proj_x, py - proj_y)

class Atom:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.z = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.symbol = symbol
        data = ELEMENTS[symbol]
        self.color = data[0]
        self.valence = data[1]
        self.mass = max(1.0, data[2])
        self.max_bonds = data[4]
        self.en = data[5]
        self.en_eff = self.en
        self.delta_charge = 0.0
        self.radius = 18 + (self.mass ** 0.3) * 2.5
        self.is_dragged = False
        
        self.hybridization = "s"
        self.shape_name = "Nedefinovano"
        self.lone_pairs = 0
        self.steric_number = 0
        self.electron_angles = [random.uniform(0, math.pi*2) for _ in range(self.valence)]
        
    def get_screen_pos(self, cam_x, cam_y, mode, view_rot_x, view_rot_y):
        if mode == MODE_2D:
            return self.x - cam_x, self.y - cam_y, self.radius, 0
        else:
            cx, cy, cz = self.x - cam_x, self.y - cam_y, self.z
            cos_x, sin_x = math.cos(view_rot_x), math.sin(view_rot_x)
            y1 = cy * cos_x - cz * sin_x
            z1 = cy * sin_x + cz * cos_x
            cos_y, sin_y = math.cos(view_rot_y), math.sin(view_rot_y)
            x2 = cx * cos_y + z1 * sin_y
            z2 = -cx * sin_y + z1 * cos_y
            
            z_dist = z2 + 800
            if z_dist < 10: z_dist = 10
            f = 800 / z_dist
            sx = x2 * f + WIDTH // 2
            sy = y1 * f + HEIGHT // 2
            return sx, sy, self.radius * f, z2

class Bond:
    def __init__(self, atom1, atom2, b_type=1):
        self.a1 = atom1
        self.a2 = atom2
        self.type = b_type
        self.rest_length = self.a1.radius + self.a2.radius + 50

class Sandbox:
    def __init__(self):
        self.atoms = []
        self.bonds = []
        self.cam_x = 0
        self.cam_y = 0
        self.current_tool = TOOL_ADD_ATOM
        self.selected_symbol = 'C'
        self.ptable_open = False
        self.mode = MODE_2D
        
        self.view_rot_x = 0.0
        self.view_rot_y = 0.0
        
        self.dragging_atom = None
        self.bonding_start_atom = None
        self.panning = False
        self.last_mouse_pos = (0,0)
        self.hovered_atom = None
        
        self.alert_message = ""
        self.alert_timer = 0
        
        self.show_electrons = True
        self.show_analysis = False
        self.analysis_text = []

        self.ui_buttons = [
            pygame.Rect(10, 10, 140, 40),
            pygame.Rect(10, 60, 140, 40),
            pygame.Rect(10, 110, 140, 40),
            pygame.Rect(10, 160, 140, 40)
        ]
        self.ui_labels = ["Kurzor", "Posun Kamery", "Pridat Atom", "Vazba"]
        self.ui_tools = [TOOL_CURSOR, TOOL_PAN, TOOL_ADD_ATOM, TOOL_ADD_BOND]
        self.btn_ptable = pygame.Rect(10, 220, 140, 100)
        
        self.btn_mode = pygame.Rect(10, HEIGHT - 70, 140, 50)
        self.btn_analysis = pygame.Rect(10, HEIGHT - 130, 140, 50)
        self.btn_electrons = pygame.Rect(10, HEIGHT - 190, 140, 50)

        # Vygenerovani statickeho pozadi
        self.static_bg = generate_vignette_bg(WIDTH, HEIGHT)
        # Jednorazove vytvoreni pruhledne vrstvy (masivni optimalizace pro Web)
        self.alpha_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def show_alert(self, text):
        self.alert_message = text
        self.alert_timer = 200

    def generate_analysis(self):
        self.analysis_text = []
        if len(self.atoms) == 0:
            self.analysis_text.append("Prostor je prazdny. Pridej nejake atomy.")
            return

        stats = {}
        for a in self.atoms:
            key = (a.symbol, a.hybridization, a.shape_name)
            stats[key] = stats.get(key, 0) + 1
            
        self.analysis_text.append(f"Celkovy pocet atomu v modelu: {len(self.atoms)}")
        self.analysis_text.append(f"Celkovy pocet vazeb: {len(self.bonds)}")
        self.analysis_text.append("-" * 40)
        self.analysis_text.append("Nalezene konfigurace atomu:")
        
        for (symbol, hyb, shape), count in stats.items():
            name = ELEMENTS[symbol][3]
            line = f"{count}x {name} ({symbol}) | {hyb} | {shape}"
            self.analysis_text.append(line)

    def calculate_chemistry(self):
        for a in self.atoms:
            a.en_eff = a.en
            
        for _ in range(3):
            temp_en = {a: a.en_eff for a in self.atoms}
            for a in self.atoms:
                if a.en == 0: continue 
                shift = 0.0
                for b in self.bonds:
                    neighbor = b.a2 if b.a1 == a else (b.a1 if b.a2 == a else None)
                    if neighbor and neighbor.en != 0:
                        shift += (temp_en[neighbor] - temp_en[a]) * 0.25 
                a.en_eff = a.en + shift

        for a in self.atoms:
            a.delta_charge = (a.en_eff - a.en) if a.en != 0 else 0.0
            
            neighbors_count = 0
            bond_orders_sum = 0
            for b in self.bonds:
                if b.a1 == a or b.a2 == a:
                    neighbors_count += 1
                    bond_orders_sum += get_bond_order(b.type)
            
            lp = (a.valence - bond_orders_sum) / 2.0
            a.lone_pairs = max(0, math.floor(lp))
            a.steric_number = neighbors_count + a.lone_pairs
            
            if neighbors_count == 0:
                a.hybridization = "s"
                a.shape_name = "Volny atom"
            elif a.steric_number <= 2:
                a.hybridization = "sp"
                a.shape_name = "Linearni tvar"
            elif a.steric_number == 3:
                a.hybridization = "sp2"
                a.shape_name = "Planarni trojuhelnik / Lomeny tvar"
            elif a.steric_number == 4:
                a.hybridization = "sp3"
                a.shape_name = "Tetraedr / Pyramida / Lomeny"
            elif a.steric_number == 5:
                a.hybridization = "sp3d"
                a.shape_name = "Trigonalni bipyramida"
            else:
                a.hybridization = "sp3d2"
                a.shape_name = "Oktaedr"

    def apply_physics(self):
        self.calculate_chemistry()

        for i in range(len(self.atoms)):
            for j in range(i+1, len(self.atoms)):
                a1, a2 = self.atoms[i], self.atoms[j]
                dx, dy, dz = a2.x - a1.x, a2.y - a1.y, a2.z - a1.z
                dist_sq = dx*dx + dy*dy + dz*dz
                
                # Optimalizace: Pokud jsou atomy moc daleko, nepocitame odpuzovani
                if dist_sq > 60000: continue
                
                dist = math.sqrt(dist_sq)
                if dist < 0.1: dist = 0.1
                
                min_dist = a1.radius + a2.radius + 30
                force = 0.0
                
                if dist < min_dist:
                    repulsion = (min_dist / dist)**2
                    force = (repulsion - 1.0) * 1.5 
                    if force > 15.0: force = 15.0
                    
                charge_factor = a1.delta_charge * a2.delta_charge * 150
                if abs(charge_factor) > 0.01 and dist < min_dist + 150:
                    c_force = charge_factor / dist
                    if c_force < -1.0: c_force = -1.0
                    if c_force > 1.0: c_force = 1.0
                    force += c_force

                if force != 0.0:
                    fx, fy, fz = (dx/dist)*force, (dy/dist)*force, (dz/dist)*force
                    if not a1.is_dragged: a1.vx -= fx/a1.mass; a1.vy -= fy/a1.mass; a1.vz -= fz/a1.mass
                    if not a2.is_dragged: a2.vx += fx/a2.mass; a2.vy += fy/a2.mass; a2.vz += fz/a2.mass

        for a in self.atoms:
            neighbors = []
            for b in self.bonds:
                if b.a1 == a: neighbors.append(b.a2)
                elif b.a2 == a: neighbors.append(b.a1)

            n_count = len(neighbors)
            if n_count < 2: continue

            base_angle = math.pi
            if a.hybridization == "sp": base_angle = math.pi
            elif a.hybridization == "sp2": base_angle = math.pi * 2/3
            elif a.hybridization == "sp3": base_angle = math.radians(109.5)
            elif a.hybridization == "sp3d": base_angle = math.pi / 2
            else: base_angle = math.pi / 2
            
            target_angle = base_angle - math.radians(a.lone_pairs * 2.5)

            for i in range(n_count):
                for j in range(i+1, n_count):
                    n1, n2 = neighbors[i], neighbors[j]
                    L1 = a.radius + n1.radius + 50
                    L2 = a.radius + n2.radius + 50
                    
                    ideal_dist = math.sqrt(L1**2 + L2**2 - 2*L1*L2*math.cos(target_angle))
                    
                    dx, dy, dz = n2.x - n1.x, n2.y - n1.y, n2.z - n1.z
                    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
                    if dist < 0.1: dist = 0.1
                    
                    diff = dist - ideal_dist
                    force = diff * 0.02
                    
                    if force > 3.0: force = 3.0
                    if force < -3.0: force = -3.0
                    
                    fx, fy, fz = (dx/dist)*force, (dy/dist)*force, (dz/dist)*force
                    
                    if not n1.is_dragged: n1.vx += fx/n1.mass; n1.vy += fy/n1.mass; n1.vz += fz/n1.mass
                    if not n2.is_dragged: n2.vx -= fx/n2.mass; n2.vy -= fy/n2.mass; n2.vz -= fz/n2.mass

        for bond in self.bonds:
            a1, a2 = bond.a1, bond.a2
            dx, dy, dz = a2.x - a1.x, a2.y - a1.y, a2.z - a1.z
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            if dist < 0.1: dist = 0.1
            
            ratio = dist / bond.rest_length
            force = (ratio - 1.0 / (ratio**2)) * 2.0
            
            if force > 8.0: force = 8.0
            if force < -8.0: force = -8.0
            
            fx, fy, fz = (dx/dist)*force, (dy/dist)*force, (dz/dist)*force
            
            if not a1.is_dragged: a1.vx += fx/a1.mass; a1.vy += fy/a1.mass; a1.vz += fz/a1.mass
            if not a2.is_dragged: a2.vx -= fx/a2.mass; a2.vy -= fy/a2.mass; a2.vz -= fz/a2.mass

        for a in self.atoms:
            if not a.is_dragged:
                a.x += a.vx; a.y += a.vy; a.z += a.vz
                
            if self.mode == MODE_2D and not a.is_dragged:
                a.z *= 0.95 
                
            a.vx *= 0.8; a.vy *= 0.8; a.vz *= 0.8

    def handle_event(self, event):
        mx, my = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if self.show_analysis:
                    self.show_analysis = False
                    return

                if self.btn_mode.collidepoint(mx, my):
                    self.mode = MODE_3D if self.mode == MODE_2D else MODE_2D
                    if self.mode == MODE_3D and len(self.atoms) > 0:
                        cx = sum(a.x for a in self.atoms) / len(self.atoms)
                        cy = sum(a.y for a in self.atoms) / len(self.atoms)
                        self.cam_x, self.cam_y = cx, cy
                        for a in self.atoms:
                            a.vz += random.uniform(-8.0, 8.0)
                    return

                if self.btn_analysis.collidepoint(mx, my):
                    self.generate_analysis()
                    self.show_analysis = True
                    return

                if self.btn_electrons.collidepoint(mx, my):
                    self.show_electrons = not self.show_electrons
                    return

                if self.mode == MODE_2D:
                    world_x, world_y = mx + self.cam_x, my + self.cam_y
                    
                    if self.ptable_open:
                        ptable_rect = pygame.Rect(160, 10, 800, 600)
                        if ptable_rect.collidepoint(mx, my):
                            cols = 6
                            w, h = 110, 80
                            keys = list(ELEMENTS.keys())
                            for i, key in enumerate(keys):
                                rx = 180 + (i % cols) * (w + 10)
                                ry = 20 + (i // cols) * (h + 10)
                                if pygame.Rect(rx, ry, w, h).collidepoint(mx, my):
                                    self.selected_symbol = key
                                    self.ptable_open = False
                                    self.current_tool = TOOL_ADD_ATOM
                                    return
                        return

                    for i, rect in enumerate(self.ui_buttons):
                        if rect.collidepoint(mx, my):
                            self.current_tool = self.ui_tools[i]
                            self.bonding_start_atom = None
                            return
                    if self.btn_ptable.collidepoint(mx, my):
                        self.ptable_open = not self.ptable_open
                        return

                    if self.ptable_open:
                        self.ptable_open = False; return

                    if self.current_tool == TOOL_PAN:
                        self.panning = True
                    elif self.current_tool == TOOL_ADD_ATOM:
                        if not self.hovered_atom:
                            if ELEMENTS[self.selected_symbol][4] == 0:
                                self.show_alert(f"KODEX: {ELEMENTS[self.selected_symbol][3]} je vzacny plyn a netvori vazby!")
                            self.atoms.append(Atom(world_x, world_y, self.selected_symbol))
                    elif self.current_tool == TOOL_CURSOR:
                        if self.hovered_atom:
                            self.dragging_atom = self.hovered_atom
                            self.dragging_atom.is_dragged = True
                    elif self.current_tool == TOOL_ADD_BOND:
                        if self.hovered_atom:
                            self.bonding_start_atom = self.hovered_atom
                
                elif self.mode == MODE_3D:
                    self.panning = True 
            
            elif event.button == 3 and self.mode == MODE_2D:
                if self.hovered_atom:
                    self.bonds = [b for b in self.bonds if b.a1 != self.hovered_atom and b.a2 != self.hovered_atom]
                    self.atoms.remove(self.hovered_atom)
                else:
                    world_x, world_y = mx + self.cam_x, my + self.cam_y
                    to_remove = None
                    for b in self.bonds:
                        dist = point_line_distance(world_x, world_y, b.a1.x, b.a1.y, b.a2.x, b.a2.y)
                        if dist < 25:
                            to_remove = b; break
                    if to_remove: self.bonds.remove(to_remove)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.panning = False
                if self.dragging_atom:
                    self.dragging_atom.is_dragged = False
                    self.dragging_atom = None
                
                if self.mode == MODE_2D and self.current_tool == TOOL_ADD_BOND and self.bonding_start_atom:
                    if self.hovered_atom and self.hovered_atom != self.bonding_start_atom:
                        start_a = self.bonding_start_atom
                        target = self.hovered_atom
                        
                        existing_bond = None
                        for b in self.bonds:
                            if (b.a1 == start_a and b.a2 == target) or (b.a2 == start_a and b.a1 == target):
                                existing_bond = b; break
                        
                        orders1 = sum(get_bond_order(b.type) for b in self.bonds if b.a1==start_a or b.a2==start_a)
                        orders2 = sum(get_bond_order(b.type) for b in self.bonds if b.a1==target or b.a2==target)
                        
                        if existing_bond:
                            next_type = existing_bond.type + 1
                            if next_type > 5: self.bonds.remove(existing_bond)
                            else:
                                diff = get_bond_order(next_type) - get_bond_order(existing_bond.type)
                                if orders1 + diff > start_a.max_bonds or orders2 + diff > target.max_bonds:
                                    self.show_alert("KODEX: Prekrocena maximalni valence atomu!")
                                else:
                                    existing_bond.type = next_type
                        else:
                            if start_a.max_bonds == 0 or target.max_bonds == 0:
                                self.show_alert("KODEX: Vzacne plyny netvori vazby!")
                            elif orders1 + 1 > start_a.max_bonds or orders2 + 1 > target.max_bonds:
                                self.show_alert("KODEX: Prekrocena maximalni valence atomu!")
                            else:
                                self.bonds.append(Bond(start_a, target))
                    self.bonding_start_atom = None

        elif event.type == pygame.MOUSEMOTION:
            if self.panning:
                dx, dy = mx - self.last_mouse_pos[0], my - self.last_mouse_pos[1]
                if self.mode == MODE_2D:
                    self.cam_x -= dx; self.cam_y -= dy
                else:
                    self.view_rot_y += dx * 0.01
                    self.view_rot_x -= dy * 0.01
            elif self.dragging_atom and self.mode == MODE_2D:
                self.dragging_atom.x = mx + self.cam_x
                self.dragging_atom.y = my + self.cam_y
                self.dragging_atom.z = 0

            self.hovered_atom = None
            if self.mode == MODE_2D:
                wx, wy = mx + self.cam_x, my + self.cam_y
                for a in reversed(self.atoms):
                    if math.hypot(a.x - wx, a.y - wy) <= a.radius + 10:
                        self.hovered_atom = a; break

        self.last_mouse_pos = (mx, my)

    def draw(self, surface, time):
        # 1. Vykresleni statickeho krasneho pozadi
        surface.blit(self.static_bg, (0, 0))
        
        # 2. Vykresleni mrizky (pohybuje se podle kamery)
        if self.mode == MODE_2D:
            gs = 100
            for x in range(int(-self.cam_x % gs), WIDTH, gs): 
                pygame.draw.line(surface, GRID_COLOR, (x,0), (x,HEIGHT))
            for y in range(int(-self.cam_y % gs), HEIGHT, gs): 
                pygame.draw.line(surface, GRID_COLOR, (0,y), (WIDTH,y))

        render_queue = []
        for a in self.atoms:
            sx, sy, sr, z = a.get_screen_pos(self.cam_x, self.cam_y, self.mode, self.view_rot_x, self.view_rot_y)
            render_queue.append({'type':'atom', 'obj': a, 'sx':sx, 'sy':sy, 'r':sr, 'z':z})
            
        for b in self.bonds:
            sx1, sy1, _, z1 = b.a1.get_screen_pos(self.cam_x, self.cam_y, self.mode, self.view_rot_x, self.view_rot_y)
            sx2, sy2, _, z2 = b.a2.get_screen_pos(self.cam_x, self.cam_y, self.mode, self.view_rot_x, self.view_rot_y)
            render_queue.append({'type':'bond', 'obj': b, 'sx1':sx1, 'sy1':sy1, 'sx2':sx2, 'sy2':sy2, 'z': (z1+z2)/2})

        render_queue.sort(key=lambda item: item['z'], reverse=True)

        # Optimalizace pro web: Nepouzivame novy povrch, jen procistime ten stavajici
        self.alpha_surface.fill((0, 0, 0, 0))

        for item in render_queue:
            if item['type'] == 'bond':
                b = item['obj']
                x1, y1, x2, y2 = item['sx1'], item['sy1'], item['sx2'], item['sy2']
                
                # Prumet orbitalu nakreslime do alfa vrstvy
                pygame.draw.line(self.alpha_surface, ORBITAL_COLOR, (x1, y1), (x2, y2), 20)
                
                dx, dy = x2 - x1, y2 - y1
                length = math.hypot(dx, dy)
                if length > 0:
                    nx, ny = -dy/length, dx/length
                    if b.type == 1 or b.type > 3: pygame.draw.line(surface, BOND_COLOR, (x1, y1), (x2, y2), 5)
                    elif b.type == 2:
                        pygame.draw.line(surface, BOND_COLOR, (x1+nx*4, y1+ny*4), (x2+nx*4, y2+ny*4), 3)
                        pygame.draw.line(surface, BOND_COLOR, (x1-nx*4, y1-ny*4), (x2-nx*4, y2-ny*4), 3)
                    elif b.type == 3:
                        pygame.draw.line(surface, BOND_COLOR, (x1+nx*6, y1+ny*6), (x2+nx*6, y2+ny*6), 2)
                        pygame.draw.line(surface, BOND_COLOR, (x1, y1), (x2, y2), 3)
                        pygame.draw.line(surface, BOND_COLOR, (x1-nx*6, y1-ny*6), (x2-nx*6, y2-ny*6), 2)

                    if self.show_electrons:
                        order = get_bond_order(b.type)
                        en_diff = b.a2.en_eff - b.a1.en_eff
                        center_shift = max(-0.4, min(0.4, en_diff * 0.15)) 
                        for i in range(order * 2):
                            osc = (math.sin(time * 4 + i * (math.pi / order)) + 1) / 2
                            t_pos = max(0.1, min(0.9, 0.2 + osc * 0.6 + center_shift))
                            ex, ey = x1 + dx * t_pos, y1 + dy * t_pos
                            side = (i % 2 - 0.5) * 8
                            pygame.draw.circle(surface, ELECTRON_COLOR, (int(ex + nx*side), int(ey + ny*side)), 2)

            elif item['type'] == 'atom':
                a = item['obj']
                sx, sy, r = int(item['sx']), int(item['sy']), max(5, int(item['r']))
                
                darken = max(0.4, min(1.0, 1.0 - (item['z'] / 800.0)))
                c = (int(a.color[0]*darken), int(a.color[1]*darken), int(a.color[2]*darken))

                if abs(a.delta_charge) > 0.05:
                    intensity = min(200, int(abs(a.delta_charge) * 400))
                    aura_c = (50, 100, 255, intensity) if a.delta_charge > 0 else (255, 50, 50, intensity)
                    pygame.draw.circle(self.alpha_surface, aura_c, (sx, sy), int(r * 2.2))

                obrys = (200, 200, 200) if a == self.hovered_atom else (20,20,20)
                pygame.draw.circle(surface, obrys, (sx, sy), r + 2)
                pygame.draw.circle(surface, c, (sx, sy), r)
                
                txt = font_element.render(a.symbol, True, (20,20,20) if sum(c)>300 else (240,240,240))
                surface.blit(txt, (sx - txt.get_width()//2, sy - txt.get_height()//2))
                
                if self.mode == MODE_2D and a.en > 0:
                    en_txt = font_tiny.render(f"{a.en:.2f}", True, get_en_color(a.en))
                    surface.blit(en_txt, (sx - en_txt.get_width()//2, sy + r + 2))
                    
        # Slouceni polopruhledne vrstvy na obrazovku
        surface.blit(self.alpha_surface, (0, 0))

        if self.mode == MODE_2D and self.current_tool == TOOL_ADD_BOND and self.bonding_start_atom:
            mx, my = pygame.mouse.get_pos()
            sx, sy, _, _ = self.bonding_start_atom.get_screen_pos(self.cam_x, self.cam_y, self.mode, 0, 0)
            pygame.draw.line(surface, (255,255,255), (sx, sy), (mx, my), 2)

        # UI
        if self.mode == MODE_2D:
            pygame.draw.rect(surface, UI_BG, (0, 0, 160, HEIGHT))
            pygame.draw.line(surface, (70,80,95), (160, 0), (160, HEIGHT), 2)
            
            mx, my = pygame.mouse.get_pos()
            for i, rect in enumerate(self.ui_buttons):
                color = UI_ACTIVE if self.current_tool == self.ui_tools[i] else (UI_HOVER if rect.collidepoint(mx, my) else (40, 45, 55))
                pygame.draw.rect(surface, color, rect, border_radius=8)
                surface.blit(font_medium.render(self.ui_labels[i], True, TEXT_COLOR), (rect.x + 10, rect.y + 8))

            color = UI_ACTIVE if self.ptable_open else (UI_HOVER if self.btn_ptable.collidepoint(mx, my) else (40, 45, 55))
            pygame.draw.rect(surface, color, self.btn_ptable, border_radius=8)
            
            edata = ELEMENTS[self.selected_symbol]
            pygame.draw.circle(surface, edata[0], (self.btn_ptable.x + 30, self.btn_ptable.y + 30), 15)
            surface.blit(font_medium.render("Aktivni:", True, (150,150,150)), (70, 225))
            surface.blit(font_large.render(self.selected_symbol, True, TEXT_COLOR), (70, 240))
            surface.blit(font_small.render(f"Valence: {edata[1]}", True, (180,180,180)), (20, 280))
            surface.blit(font_small.render(f"EN: {edata[5]:.2f}", True, get_en_color(edata[5])), (20, 300))

            if self.ptable_open:
                ptable_rect = pygame.Rect(160, 10, 800, 600)
                pygame.draw.rect(surface, UI_BG, ptable_rect, border_radius=10)
                pygame.draw.rect(surface, (70,80,95), ptable_rect, width=2, border_radius=10)
                cols = 6
                for i, (sym, data) in enumerate(ELEMENTS.items()):
                    rx = 180 + (i % cols) * 120
                    ry = 20 + (i // cols) * 90
                    rect = pygame.Rect(rx, ry, 110, 80)
                    bg_col = UI_ACTIVE if sym == self.selected_symbol else (UI_HOVER if rect.collidepoint(mx, my) else (40, 45, 55))
                    pygame.draw.rect(surface, bg_col, rect, border_radius=5)
                    pygame.draw.circle(surface, data[0], (rx + 25, ry + 25), 12)
                    surface.blit(font_element.render(sym, True, TEXT_COLOR), (rx + 45, ry + 10))
                    surface.blit(font_small.render(data[3], True, (180,180,180)), (rx + 10, ry + 40))
                    surface.blit(font_small.render(f"EN: {data[5]:.2f}", True, get_en_color(data[5])), (rx + 10, ry + 55))

        # Leve spodni tlacitka
        mx, my = pygame.mouse.get_pos()
        
        pygame.draw.rect(surface, (100, 70, 160) if self.mode == MODE_3D else (60, 110, 180), self.btn_mode, border_radius=8)
        mode_txt = "-> Zpet do 2D" if self.mode == MODE_3D else "-> 3D Prohlidka"
        surface.blit(font_medium.render(mode_txt, True, WHITE), (self.btn_mode.x + 10, self.btn_mode.y + 12))

        el_col = (70, 160, 110) if self.show_electrons else (160, 70, 70)
        pygame.draw.rect(surface, el_col, self.btn_electrons, border_radius=8)
        el_txt = "Elektrony ON" if self.show_electrons else "Elektrony OFF"
        surface.blit(font_medium.render(el_txt, True, WHITE), (self.btn_electrons.x + 10, self.btn_electrons.y + 12))

        pygame.draw.rect(surface, (160, 120, 60), self.btn_analysis, border_radius=8)
        surface.blit(font_medium.render("Analyza Molekuly", True, WHITE), (self.btn_analysis.x + 5, self.btn_analysis.y + 12))

        if self.mode == MODE_3D:
            surface.blit(font_large.render("3D Prohlidka (Tazenim otacej)", True, (150, 200, 255)), (180, 20))

        if self.show_analysis:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, (0, 0))
            
            win_w, win_h = 700, 500
            win_x, win_y = WIDTH//2 - win_w//2, HEIGHT//2 - win_h//2
            
            pygame.draw.rect(surface, (25, 30, 40), (win_x, win_y, win_w, win_h), border_radius=15)
            pygame.draw.rect(surface, (100, 150, 255), (win_x, win_y, win_w, win_h), width=2, border_radius=15)
            
            title = font_large.render("VSEPR Model a Hybridizace", True, WHITE)
            surface.blit(title, (win_x + win_w//2 - title.get_width()//2, win_y + 20))
            
            y_offset = win_y + 80
            for line in self.analysis_text:
                txt = font_medium.render(line, True, (200, 220, 255))
                surface.blit(txt, (win_x + 30, y_offset))
                y_offset += 30
                
            close_txt = font_medium.render("Kliknutim kamkoliv okno zavres", True, (150, 150, 150))
            surface.blit(close_txt, (win_x + win_w//2 - close_txt.get_width()//2, win_y + win_h - 40))

        if self.hovered_atom and self.mode == MODE_2D and not self.show_analysis:
            ha = self.hovered_atom
            info_h = 110
            pygame.draw.rect(surface, (20, 25, 35), (WIDTH - 280, 20, 260, info_h), border_radius=10)
            pygame.draw.rect(surface, (100, 150, 255), (WIDTH - 280, 20, 260, info_h), width=2, border_radius=10)
            
            surface.blit(font_element.render(f"Atom: {ha.symbol}", True, ha.color), (WIDTH - 260, 30))
            surface.blit(font_small.render(f"Hybridizace: {ha.hybridization}", True, WHITE), (WIDTH - 260, 60))
            surface.blit(font_small.render(f"Volne pary: {ha.lone_pairs}", True, WHITE), (WIDTH - 260, 80))
            surface.blit(font_small.render(f"Delta naboj: {ha.delta_charge:+.2f}", True, WHITE), (WIDTH - 260, 100))

        if self.alert_timer > 0:
            alert_surf = font_alert.render(self.alert_message, True, ALERT_COLOR)
            bg_rect = pygame.Rect(WIDTH//2 - alert_surf.get_width()//2 - 10, 30, alert_surf.get_width() + 20, 40)
            pygame.draw.rect(surface, (30, 20, 20), bg_rect, border_radius=8)
            pygame.draw.rect(surface, ALERT_COLOR, bg_rect, width=2, border_radius=8)
            surface.blit(alert_surf, (WIDTH//2 - alert_surf.get_width()//2, 35))
            self.alert_timer -= 1

async def main():
    sandbox = Sandbox()
    time = 0.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            sandbox.handle_event(event)

        sandbox.apply_physics()
        time += 0.05
        sandbox.draw(screen, time)

        pygame.display.flip()
        clock.tick(60)
        
        # Tento radek udrzuje web a prohlizec pri zivote
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
