import sys
import solar_corr
import warnings


if __name__ == "__main__":
	warnings.filterwarnings("ignore")
    image_path = sys.argv[3] if len(sys.argv) > 3 else "solar.png" 
    solar_corr.main(sys.argv[1], sys.argv[2], image_path)