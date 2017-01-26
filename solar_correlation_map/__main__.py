import sys
import solar_corr

import warnings

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    try:
        image_path = sys.argv[3] if len(sys.argv) > 3 else "solar.png"
        solar_corr.main(sys.argv[1], sys.argv[2], image_path)
    except:
        print("python -m solar_correlation_map [csv-file-name] [central-variable]")
        print("example: python -m solar_correlation_map jedi.csv JEDI")
