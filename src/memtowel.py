"""Clean up those memory leaks."""

import os
import psutil
from mpi4py import MPI
import numpy as np


class MemoryTowel:
    """Measure and save memory used by all processes."""

    def __init__(self, comm=MPI.COMM_WORLD, filename="memory.txt"):
        self.comm = comm
        self.comm_rank = comm.rank
        self.comm_size = comm.size
        self.filename = filename
        self.process = psutil.Process(os.getpid())
        self.write_number = 0
        self._sendbuf = np.zeros(1, dtype=int)
        if self.comm_rank == 0:
            self._recvbuf = np.zeros([self.comm_size, 1], dtype=int)
            self._recvflat = self._recvbuf.ravel()
        else:
            self._recvbuf = None
            self._recvflat = None

    def process_memory(self):
        """Measure memory usage by current process."""
        return self.process.memory_info()[0]

    def comm_memory(self):
        """Gather memory usage by each process."""
        if self.comm_size == 1:
            return np.array([self.process_memory()], dtype=int)
        else:
            self._sendbuf[0] = self.process_memory()
            self.comm.Gather(self._sendbuf, self._recvbuf, root=0)
            return self._recvflat

    def print_comm_memory(self, label=None):
        """Print comm memory."""
        comm_memory = self.comm_memory()
        if self.comm_rank == 0:
            if label is None:
                print(comm_memory)
            else:
                print(f"{label} {comm_memory}")

    def write_comm_memory(self, label=None):
        """Save comm memory."""
        comm_memory = self.comm_memory()
        if self.comm_rank == 0:
            if label is None:
                label = self.write_number
            if self.write_number == 0:
                mode = "w"
            else:
                mode = "a"
            with open(self.filename, mode) as file:
                file.write(f"{label} {comm_memory}\n")
        self.write_number += 1


if __name__ == '__main__':
    # Test the towel
    memtowel = MemoryTowel()
    a = np.random.random((512,512,512))
    memtowel.print_comm_memory(label='one array ')
    b = np.random.random((512,512,512))
    memtowel.print_comm_memory(label='two arrays')
    del b
    memtowel.print_comm_memory(label='one array ')

