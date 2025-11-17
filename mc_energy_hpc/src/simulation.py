import math
import random
import time
from dataclasses import dataclass
from typing import Tuple

Vec3 = Tuple[float, float, float]


@dataclass
class Atom:
    pos: Vec3


class MonteCarloSim:
    def __init__(self, n_atoms: int = 30, temp: float = 1.0, seed: int = 0, max_steps: int = 10000, max_move: float = 0.1) -> None:
        self.n = n_atoms
        self.temp = temp
        self.seed = seed
        self.max_steps = max_steps
        self.max_move = max_move
        random.seed(seed)
        self.atoms = [Atom((i * 1.0, 0.0, 0.0)) for i in range(self.n)]

    def bond_energy(self, p1: Vec3, p2: Vec3, k: float = 1.0, r0: float = 1.0) -> float:
        dx, dy, dz = p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2]
        r = math.sqrt(dx * dx + dy * dy + dz * dz)
        return 0.5 * k * (r - r0) ** 2

    def total_energy(self) -> float:
        return sum(self.bond_energy(self.atoms[i].pos, self.atoms[i + 1].pos) for i in range(self.n - 1))

    def random_move(self) -> Tuple[int, Vec3, Vec3]:
        i = random.randrange(self.n)
        dx = (random.random() * 2 - 1) * self.max_move
        dy = (random.random() * 2 - 1) * self.max_move
        dz = (random.random() * 2 - 1) * self.max_move
        old_pos = self.atoms[i].pos
        new_pos = (old_pos[0] + dx, old_pos[1] + dy, old_pos[2] + dz)
        return i, old_pos, new_pos

    def step(self) -> None:
        i, old_pos, new_pos = self.random_move()
        e_old = 0.0
        e_new = 0.0
        if i - 1 >= 0:
            e_old += self.bond_energy(old_pos, self.atoms[i - 1].pos)
            e_new += self.bond_energy(new_pos, self.atoms[i - 1].pos)
        if i + 1 < self.n:
            e_old += self.bond_energy(old_pos, self.atoms[i + 1].pos)
            e_new += self.bond_energy(new_pos, self.atoms[i + 1].pos)
        delta = e_new - e_old
        if delta <= 0 or random.random() < math.exp(-delta / max(self.temp, 1e-12)):
            self.atoms[i].pos = new_pos

    def run(self, record_every: int = 1000):
        energies = []
        t0 = time.time()
        for step in range(self.max_steps):
            self.step()
            if step % record_every == 0:
                energies.append((step, self.total_energy()))
        t1 = time.time()
        return {
            "seed": self.seed,
            "n_atoms": self.n,
            "max_steps": self.max_steps,
            "time_s": t1 - t0,
            "energies": energies,
        }


__all__ = ["Atom", "MonteCarloSim"]
