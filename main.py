import asyncio
import sys
import pygame

# Inisialisasi Pygame
pygame.init()

# Ukuran Layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Newlands' Octave Challenge - 3 Rounds")

# Palet Warna Cerah & Colorful (Neon / Vibrant)
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
COLOR_NEON_YELLOW = (255, 230, 0)
COLOR_NEON_CYAN = (0, 245, 255)
COLOR_NEON_PINK = (255, 20, 147)
COLOR_NEON_GREEN = (0, 255, 127)
COLOR_NEON_ORANGE = (255, 140, 0)
COLOR_CARD_BG = (255, 255, 255)

# Font
font_title = pygame.font.SysFont("Arial", 32, bold=True)
font_btn = pygame.font.SysFont("Arial", 22, bold=True)
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 16)

# --- LOAD GAMBAR (Background & Avatar) ---
try:
  bg_image = pygame.image.load("lab_bg.jpg")
  bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except:
  bg_image = None

try:
  avatar_image = pygame.image.load("newlands.png.png")
  avatar_image = pygame.transform.scale(avatar_image, (100, 140))
except:
  avatar_image = None

# Status Game & Round
game_state = 0
score = 0
feedback_msg = ""

# Data Kartu per Round (valid: True = Benar/Utama, valid: False = Jebakan/Salah)
round1_cards = [
    {
        "name": "H (Massa 1)",
        "x": 100,
        "y": 420,
        "orig_x": 100,
        "orig_y": 420,
        "valid": True,
    },
    {
        "name": "Li (Massa 7)",
        "x": 250,
        "y": 420,
        "orig_x": 250,
        "orig_y": 420,
        "valid": True,
    },
    {
        "name": "Be (Massa 9)",
        "x": 400,
        "y": 420,
        "orig_x": 400,
        "orig_y": 420,
        "valid": True,
    },
    {
        "name": "B (Massa 11)",
        "x": 550,
        "y": 420,
        "orig_x": 550,
        "orig_y": 420,
        "valid": True,
    },
]

round2_cards = [
    {
        "name": "Na (Mirip Li)",
        "x": 200,
        "y": 420,
        "orig_x": 200,
        "orig_y": 420,
        "valid": True,
    },
    {
        "name": "Fe (Unsur Berat)",
        "x": 450,
        "y": 420,
        "orig_x": 450,
        "orig_y": 420,
        "valid": False,
    },  # Jebakan (harus dimasukkan setelah Na)
]

round3_cards = [
    {
        "name": "Cl (Klorin)",
        "x": 200,
        "y": 420,
        "orig_x": 200,
        "orig_y": 420,
        "valid": True,
    },
    {
        "name": "Fe (Besi - Berat)",
        "x": 450,
        "y": 420,
        "orig_x": 450,
        "orig_y": 420,
        "valid": False,
    },  # Jebakan/Kelemahan
]

current_cards = []
selected_card = None

# Loop Utama Game
clock = pygame.time.Clock()

while True:
  # Background
  if bg_image:
    screen.blit(bg_image, (0, 0))
  else:
    screen.fill((20, 15, 45))

  # Event Handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    elif event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()

      if game_state == 0:
        if 250 <= pos[0] <= 550 and 380 <= pos[1] <= 450:
          game_state = 1
          score = 0

      elif game_state in [1, 3, 5]:
        if 250 <= pos[0] <= 550 and 420 <= pos[1] <= 490:
          feedback_msg = ""
          if game_state == 1:
            game_state = 2
            current_cards = [card.copy() for card in round1_cards]
          elif game_state == 3:
            game_state = 4
            current_cards = [card.copy() for card in round2_cards]
          elif game_state == 5:
            game_state = 6
            current_cards = [card.copy() for card in round3_cards]

      elif game_state in [2, 4, 6]:
        for card in current_cards:
          if (
              card["x"] <= pos[0] <= card["x"] + 130
              and card["y"] <= pos[1] <= card["y"] + 75
          ):
            selected_card = card

      elif game_state == 7:
        if 280 <= pos[0] <= 520 and 420 <= pos[1] <= 490:
          game_state = 0

    elif event.type == pygame.MOUSEBUTTONUP:
      if game_state in [2, 4, 6] and selected_card:
        pos = pygame.mouse.get_pos()
        if 180 <= pos[0] <= 620 and 150 <= pos[1] <= 280:
          is_correct = False

          if game_state == 2:
            if current_cards[0]["name"] == selected_card["name"]:
              is_correct = True
          elif game_state in [4, 6]:
            # Cek apakah masih ada kartu yang 'valid: True' (jawaban benar utama) di layar
            other_valid_exists = any(
                c["valid"] for c in current_cards if c != selected_card
            )

            if selected_card["valid"]:
              is_correct = True
            else:
              # Ini kartu salah/jebakan (valid: False)
              if other_valid_exists:
                # Belum boleh dimasukkan jika kartu yang benar belum dimasukkan
                selected_card["x"] = selected_card["orig_x"]
                selected_card["y"] = selected_card["orig_y"]
                feedback_msg = (
                    "Masukkan unsur yang benar dulu sebelum menandai jebakan!"
                )
                selected_card = None
                continue
              else:
                # Kartu jebakan baru bisa dimasukkan SETELAH kartu yang benar habis
                is_correct = True

          if is_correct:
            if game_state in [4, 6] and not selected_card["valid"]:
              # Ditandai sebagai jawaban salah/jebakan yang berhasil diidentifikasi
              feedback_msg = (
                  "Ditandai: Fe adalah unsur jebakan (tidak sesuai"
                  " oktaf)!"
              )
            else:
              score += 30
              feedback_msg = "Benar! Bagus sekali."
            current_cards.remove(selected_card)
          else:
            selected_card["x"] = selected_card["orig_x"]
            selected_card["y"] = selected_card["orig_y"]
            feedback_msg = "Ups, urutan salah! Coba lagi."

          selected_card = None

          # Pindah ke tahap berikutnya jika kartu habis
          if len(current_cards) == 0:
            if game_state == 2:
              game_state = 3  # Intro Round 2
            elif game_state == 4:
              game_state = 5  # Intro Round 3
            elif game_state == 6:
              game_state = 7  # Selesai
        else:
          selected_card["x"] = selected_card["orig_x"]
          selected_card["y"] = selected_card["orig_y"]
          selected_card = None

  # --- TAMPILAN ANTARMUKA ---
  if game_state == 0:
    title_box = pygame.Surface((620, 120), pygame.SRCALPHA)
    title_box.fill((20, 20, 40, 210))
    screen.blit(title_box, (90, 150))
    import asyncio
import sys
import pygame

# Inisialisasi Pygame
pygame.init()

# Ukuran Layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Newlands' Octave Challenge - 3 Rounds")

# Palet Warna Cerah & Colorful (Neon / Vibrant)
WHITE = (255, 255, 255)
BLACK = (20, 20, 30)
COLOR_NEON_YELLOW = (255, 230, 0)
COLOR_NEON_CYAN = (0, 245, 255)
COLOR_NEON_PINK = (255, 20, 147)
COLOR_NEON_GREEN = (0, 255, 127)
COLOR_NEON_ORANGE = (255, 140, 0)
COLOR_CARD_BG = (255, 255, 255)

# Font
font_title = pygame.font.SysFont("Arial", 28, bold=True)
font_btn = pygame.font.SysFont("Arial", 20, bold=True)
font_medium = pygame.font.SysFont("Arial", 18, bold=True)
font_small = pygame.font.SysFont("Arial", 15)

# --- LOAD GAMBAR (Background & Avatar) ---
try:
  bg_image = pygame.image.load("lab_bg.jpg")
  bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except:
  bg_image = None

try:
  avatar_image = pygame.image.load("newlands.png.png")
  avatar_image = pygame.transform.scale(avatar_image, (100, 140))
except:
  avatar_image = None

# Status Game & Round
game_state = 0
score = 0
feedback_msg = ""

# Data Kartu per Round
round1_cards = [
    {
        "name": "H (Massa 1)",
        "x": 100,
        "y": 480,
        "orig_x": 100,
        "orig_y": 480,
        "valid": True,
    },
    {
        "name": "Li (Massa 7)",
        "x": 250,
        "y": 480,
        "orig_x": 250,
        "orig_y": 480,
        "valid": True,
    },
    {
        "name": "Be (Massa 9)",
        "x": 400,
        "y": 480,
        "orig_x": 400,
        "orig_y": 480,
        "valid": True,
    },
    {
        "name": "B (Massa 11)",
        "x": 550,
        "y": 480,
        "orig_x": 550,
        "orig_y": 480,
        "valid": True,
    },
]

round2_cards = [
    {
        "name": "Na (Mirip Li)",
        "x": 250,
        "y": 480,
        "orig_x": 250,
        "orig_y": 480,
        "valid": True,
    },
    {
        "name": "Fe (Unsur Berat)",
        "x": 450,
        "y": 480,
        "orig_x": 450,
        "orig_y": 480,
        "valid": False,
    },
]

round3_cards = [
    {
        "name": "Cl (Klorin)",
        "x": 250,
        "y": 480,
        "orig_x": 250,
        "orig_y": 480,
        "valid": True,
    },
    {
        "name": "Fe (Besi - Berat)",
        "x": 450,
        "y": 480,
        "orig_x": 450,
        "orig_y": 480,
        "valid": False,
    },
]

current_cards = []
selected_card = None

# Clock
clock = pygame.time.Clock()


# Loop Utama Game (Asynchronous)
async def main():
  global game_state, score, feedback_msg, current_cards, selected_card

  while True:
    # 1. Background
    if bg_image:
      screen.blit(bg_image, (0, 0))
    else:
      screen.fill((20, 15, 45))

    # 2. Event Handling
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      elif event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()

        # State 0: Main Menu -> Tombol Mulai Eksperimen
        if game_state == 0:
          if 250 <= pos[0] <= 550 and 380 <= pos[1] <= 450:
            game_state = 1
            score = 0

        # State 1, 3, 5: Intro Round -> Tombol Lanjut Eksperimen
        elif game_state in [1, 3, 5]:
          if 250 <= pos[0] <= 550 and 420 <= pos[1] <= 480:
            feedback_msg = ""
            if game_state == 1:
              game_state = 2
              current_cards = [card.copy() for card in round1_cards]
            elif game_state == 3:
              game_state = 4
              current_cards = [card.copy() for card in round2_cards]
            elif game_state == 5:
              game_state = 6
              current_cards = [card.copy() for card in round3_cards]

        # State 2, 4, 6: Gameplay (Pilih Kartu)
        elif game_state in [2, 4, 6]:
          for card in current_cards:
            if (
                card["x"] <= pos[0] <= card["x"] + 130
                and card["y"] <= pos[1] <= card["y"] + 75
            ):
              selected_card = card

        # State 7: Selesai -> Tombol Main Lagi
        elif game_state == 7:
          if 280 <= pos[0] <= 520 and 420 <= pos[1] <= 490:
            game_state = 0

      elif event.type == pygame.MOUSEBUTTONUP:
        if game_state in [2, 4, 6] and selected_card:
          pos = pygame.mouse.get_pos()
          # Area Drop Zone di tengah atas
          if 180 <= pos[0] <= 620 and 130 <= pos[1] <= 250:
            is_correct = False

            if game_state == 2:
              if current_cards[0]["name"] == selected_card["name"]:
                is_correct = True
            elif game_state in [4, 6]:
              other_valid_exists = any(
                  c["valid"] for c in current_cards if c != selected_card
              )

              if selected_card["valid"]:
                is_correct = True
              else:
                if other_valid_exists:
                  selected_card["x"] = selected_card["orig_x"]
                  selected_card["y"] = selected_card["orig_y"]
                  feedback_msg = (
                      "Masukkan unsur yang benar dulu sebelum menandai jebakan!"
                  )
                  selected_card = None
                  continue
                else:
                  is_correct = True

            if is_correct:
              if game_state in [4, 6] and not selected_card["valid"]:
                feedback_msg = (
                    "Ditandai: Fe adalah unsur jebakan (tidak sesuai"
                    " oktaf)!"
                )
              else:
                score += 30
                feedback_msg = "Benar! Bagus sekali."
              current_cards.remove(selected_card)
            else:
              selected_card["x"] = selected_card["orig_x"]
              selected_card["y"] = selected_card["orig_y"]
              feedback_msg = "Ups, urutan salah! Coba lagi."

            selected_card = None

            # Pindah round jika kartu habis
            if len(current_cards) == 0:
              if game_state == 2:
                game_state = 3
              elif game_state == 4:
                game_state = 5
              elif game_state == 6:
                game_state = 7
          else:
            selected_card["x"] = selected_card["orig_x"]
            selected_card["y"] = selected_card["orig_y"]
            selected_card = None

    # 3. TAMPILAN ANTARMUKA (RENDER SECTION)
    if game_state == 0:
      # Menu Utama
      title_box = pygame.Surface((620, 120), pygame.SRCALPHA)
      title_box.fill((20, 20, 40, 210))
      screen.blit(title_box, (90, 150))
      pygame.draw.rect(
          screen, COLOR_NEON_YELLOW, (90, 150, 620, 120), 2, border_radius=15
      )

      title = font_title.render(
          "NEWLANDS' OCTAVE CHALLENGE", True, COLOR_NEON_YELLOW
      )
      sub = font_medium.render(
          "Lab Kimia SPU - Petualangan 3 Round Unik!", True, COLOR_NEON_CYAN
      )
      screen.blit(title, (WIDTH / 2 - title.get_width() / 2, 170))
      screen.blit(sub, (WIDTH / 2 - sub.get_width() / 2, 220))

      pygame.draw.rect(
          screen, COLOR_NEON_GREEN, (250, 380, 300, 70), border_radius=20
      )
      pygame.draw.rect(screen, WHITE, (250, 380, 300, 70), 3, border_radius=20)
      btn_text = font_btn.render("MULAI EKSPERIMEN", True, BLACK)
      screen.blit(btn_text, (WIDTH / 2 - btn_text.get_width() / 2, 402))

    elif game_state in [1, 3, 5]:
      # Layar Pengantar Round
      box_intro = pygame.Surface((700, 320), pygame.SRCALPHA)
      box_intro.fill((30, 20, 60, 230))
      screen.blit(box_intro, (50, 80))
      pygame.draw.rect(
          screen, COLOR_NEON_CYAN, (50, 80, 700, 320), 3, border_radius=15
      )

      if game_state == 1:
        round_title = "PENGANTAR ROUND 1"
        desc = (
            "John Newlands menyusun unsur berdasarkan\nkenaikan massa atom."
            " Mari kita mulai\ndengan menyusun unsur-unsur ringan\npertama"
            " secara berurutan (dari Hidrogen)."
        )
      elif game_state == 3:
        round_title = "PENGANTAR ROUND 2 (Hukum Oktaf)"
        desc = (
            "Masukkan dulu unsur yang benar (Na),\nbaru kemudian masukkan unsur"
            " jebakan (Fe)\nuntuk menandainya sebagai pengecualian/salah!"
        )
      else:
        round_title = "PENGANTAR ROUND 3 (Uji Kelemahan)"
        desc = (
            "Uji kelemahan teori Newlands!\nMasukkan unsur yang benar (Cl) dulu,"
            "\nlalu tandai unsur berat (Fe) sebagai keliru."
        )

      r_title_surf = font_title.render(round_title, True, COLOR_NEON_YELLOW)
      screen.blit(r_title_surf, (80, 110))

      for i, line in enumerate(desc.split("\n")):
        d_surf = font_medium.render(line, True, WHITE)
        screen.blit(d_surf, (80, 170 + (i * 30)))

      pygame.draw.rect(
          screen, COLOR_NEON_ORANGE, (250, 420, 300, 60), border_radius=15
      )
      pygame.draw.rect(
          screen, WHITE, (250, 420, 300, 60), 2, border_radius=15
      )
      l_text = font_btn.render("LANJUT EKSPERIMEN", True, BLACK)
      screen.blit(l_text, (WIDTH / 2 - l_text.get_width() / 2, 438))

    else:
      # Area Gameplay Aktif (States 2, 4, 6)
      pygame.draw.rect(
          screen, (40, 30, 80), (30, 320, 120, 160), border_radius=15
      )
      pygame.draw.rect(
          screen, COLOR_NEON_PINK, (30, 320, 120, 160), 3, border_radius=15
      )

      if avatar_image:
        screen.blit(avatar_image, (40, 330))
      else:
        avatar_title = font_small.render("👨‍🔬 Newlands", True, COLOR_NEON_YELLOW)
        screen.blit(avatar_title, (40, 380))

      pygame.draw.rect(
          screen, (255, 255, 255), (160, 320, 320, 100), border_radius=12
      )
      pygame.draw.rect(
          screen, COLOR_NEON_CYAN, (160, 320, 320, 100), 3, border_radius=12
      )

      if game_state == 2:
        dialog = "Susun unsur ringan\ndari H (Massa 1) dulu ya!"
      elif game_state == 4:
        dialog = "Masukkan Na dulu,\nbaru tandai Fe sebagai jebakan!"
      else:
        dialog = "Masukkan Cl dulu,\nlalu tandai Fe yang tidak cocok!"

      for i, line in enumerate(dialog.split("\n")):
        d_txt = font_small.render(line, True, BLACK)
        screen.blit(d_txt, (175, 340 + (i * 22)))

      if game_state == 2:
        header_txt = "ROUND 1: Menyusun Unsur Berurutan"
      elif game_state == 4:
        header_txt = "ROUND 2: Membuktikan Hukum Oktaf"
      else:
        header_txt = "ROUND 3: Uji Kelemahan Unsur Berat"

      h_surf = font_title.render(header_txt, True, COLOR_NEON_YELLOW)
      screen.blit(h_surf, (WIDTH / 2 - h_surf.get_width() / 2, 30))

      sc = font_medium.render(f"Skor: {score}", True, COLOR_NEON_GREEN)
      screen.blit(sc, (30, 35))

      if feedback_msg:
        f_surf = font_medium.render(feedback_msg, True, COLOR_NEON_PINK)
        screen.blit(f_surf, (WIDTH / 2 - f_surf.get_width() / 2, 85))

      pygame.draw.rect(
          screen, (50, 40, 90), (180, 130, 440, 120), border_radius=15
      )
      pygame.draw.rect(
          screen, COLOR_NEON_ORANGE, (180, 130, 440, 120), 3, border_radius=15
      )
      slot_lbl = font_medium.render(
          "🧪 TARUH KARTU UNSUR DI SINI 🧪", True, COLOR_NEON_ORANGE
      )
      screen.blit(slot_lbl, (215, 175))

      for card in current_cards:
        pygame.draw.rect(
            screen,
            COLOR_CARD_BG,
            (card["x"], card["y"], 130, 75),
            0,
            12,
        )
        pygame.draw.rect(
            screen,
            COLOR_NEON_CYAN,
            (card["x"], card["y"], 130, 75),
            3,
            12,
        )
        c_txt = font_small.render(card["name"], True, BLACK)
        screen.blit(c_txt, (card["x"] + 12, card["y"] + 27))

      if selected_card:
        m_pos = pygame.mouse.get_pos()
        selected_card["x"] = m_pos[0] - 65
        selected_card["y"] = m_pos[1] - 37

    # Layar Selesai (State 7)
    if game_state == 7:
      fin = font_title.render(
          "🎉 LUAR BIASA! 3 ROUND SELESAI!", True, COLOR_NEON_YELLOW
      )
      sc_fin = font_medium.render(
          f"Total Skor Akhir Kamu: {score}", True, COLOR_NEON_GREEN
      )
      screen.blit(fin, (WIDTH / 2 - fin.get_width() / 2, 200))
      screen.blit(sc_fin, (WIDTH / 2 - sc_fin.get_width() / 2, 260))

      pygame.draw.rect(
          screen, COLOR_NEON_PINK, (280, 420, 240, 70), border_radius=20
      )
      pygame.draw.rect(screen, WHITE, (280, 420, 240, 70), 3, border_radius=20)
      res_txt = font_btn.render("MAIN LAGI", True, WHITE)
      screen.blit(res_txt, (WIDTH / 2 - res_txt.get_width() / 2, 440))

    pygame.display.flip()
    await asyncio.sleep(0)
    clock.tick(60)


if __name__ == "__main__":
  asyncio.run(main())