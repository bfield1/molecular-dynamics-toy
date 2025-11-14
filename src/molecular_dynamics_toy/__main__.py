"""Entry point for running the package as a module."""

import multiprocessing

from molecular_dynamics_toy.app import main

if __name__ == "__main__":
    # https://stackoverflow.com/a/32677108
    multiprocessing.freeze_support()

    main()