class TestAnimation:

    def get_duration_in_ms(self):
        return 3000

    def reset(self):
        print("Reset")
        self.x = 10

    def update(self, elapsed_ms):
        print(f"Update {elapsed_ms}")
        self.x += elapsed_ms*0.1

    def draw(self, surface):
        surface.fill_rect(self.x, 10, 10, 10, (0.1, 0.5, 0.8))
