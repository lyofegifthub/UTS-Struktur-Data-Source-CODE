import pandas as pd

def get_csv_export_link(google_sheet_url):
    """Mengubah Google Sheets URL menjadi URL export CSV"""
    try:
        file_id = google_sheet_url.split("/d/")[1].split("/")[0]
        gid = google_sheet_url.split("gid=")[1]
        export_link = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv&gid={gid}"
        return export_link
    except:
        print("URL Google Sheets tidak valid.")
        return None

def load_data(source='local', file_path=None, sheet_url=None):
    """Memuat data dari file lokal atau Google Sheets"""
    try:
        if source == 'google':
            export_link = get_csv_export_link(sheet_url)
            if export_link is None:
                return None
            df = pd.read_csv(export_link)
        else:
            df = pd.read_excel(file_path)

        # Ubah nama kolom agar seragam
        df.rename(columns={
            "Judul Paper": "Judul",
            "Nama Penulis": "Penulis",
            "Tahun Terbit": "Tahun"
        }, inplace=True)

        df['Tahun'] = pd.to_numeric(df['Tahun'], errors='coerce').fillna(0).astype(int)
        return df
    except Exception as e:
        print(f"Error saat memuat data: {e}")
        return None

def linear_search(data, keyword, field):
    results = []
    keyword = str(keyword).lower()
    
    for _, row in data.iterrows():
        cell_value = str(row[field]).lower()
        if keyword in cell_value:
            results.append(row)
    
    return pd.DataFrame(results)

def binary_search(data, keyword, field):
    search_data = data.copy()
    search_data['search_field'] = search_data[field].astype(str).str.lower()
    search_data = search_data.sort_values(by='search_field')
    
    results = []
    keyword = str(keyword).lower()
    n = len(search_data)
    
    left, right = 0, n - 1
    found_index = -1
    
    while left <= right:
        mid = (left + right) // 2
        mid_val = search_data.iloc[mid]['search_field']
        
        if keyword in mid_val:
            found_index = mid
            break
        elif mid_val < keyword:
            left = mid + 1
        else:
            right = mid - 1
    
    if found_index != -1:
        i = found_index
        while i >= 0 and keyword in search_data.iloc[i]['search_field']:
            results.append(search_data.iloc[i])
            i -= 1
        
        i = found_index + 1
        while i < n and keyword in search_data.iloc[i]['search_field']:
            results.append(search_data.iloc[i])
            i += 1
    
    return pd.DataFrame(results)

def display_results(results, keyword):
    if results.empty:
        print(f"\nTidak ditemukan hasil untuk '{keyword}'")
    else:
        print(f"\nDitemukan {len(results)} hasil untuk '{keyword}':")
        print("=" * 70)
        for _, row in results.iterrows():
            print(f"Judul   : {row['Judul']}")
            print(f"Penulis : {row['Penulis']}")
            print(f"Tahun   : {row['Tahun']}")
            print("-" * 70)

def main():
    print("Pilih sumber data:")
    print("1. File Lokal")
    print("2. Google Sheets Online")
    source_choice = input("Masukkan pilihan (1/2): ")

    if source_choice == '2':
        sheet_url = "https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/edit?gid=743838712"
        data = load_data(source='google', sheet_url=sheet_url)
    else:
        file_path = r"D:\TUGAS KULIAH\program strukdat\paperdata.xlsx"
        data = load_data(source='local', file_path=file_path)

    if data is None:
        return

    print(f"Data berhasil dimuat. Total {len(data)} artikel.")
    
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Linear Search (partial match)")
        print("2. Binary Search (partial match)")
        print("3. Keluar")
        
        choice = input("Pilih metode pencarian (1/2/3): ")
        
        if choice == '3':
            print("Program selesai.")
            break
        elif choice not in ['1', '2']:
            print("Pilihan tidak valid!")
            continue
            
        print("\nPilih bidang pencarian:")
        print("1. Judul")
        print("2. Penulis")
        print("3. Tahun")
        
        field_choice = input("Masukkan pilihan (1/2/3): ")
        
        if field_choice == '1':
            field = 'Judul'
        elif field_choice == '2':
            field = 'Penulis'
        elif field_choice == '3':
            field = 'Tahun'
        else:
            print("Pilihan tidak valid!")
            continue
            
        keyword = input(f"Masukkan kata kunci ({field}): ").strip()
        
        if choice == '1':
            results = linear_search(data, keyword, field)
        else:
            results = binary_search(data, keyword, field)
        
        display_results(results, keyword)
        
        if input("\nCari lagi? (y/n): ").lower() != 'y':
            print("Program selesai.")
            break

if __name__ == "__main__":
    main()
