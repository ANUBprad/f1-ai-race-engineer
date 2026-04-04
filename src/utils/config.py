import fastf1
import os

def setup_fastf1_cache(cache_dir: str = "data/cache"):
    """
    Initialize FastF1 cache directory.
    Ensures faster repeated data loading.
    """
    os.makedirs(cache_dir, exist_ok=True)
    fastf1.Cache.enable_cache(cache_dir)