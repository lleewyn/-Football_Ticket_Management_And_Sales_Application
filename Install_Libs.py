import subprocess

def install_requirements():
    print("Đang cài đặt các thư viện...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
    print("Cài đặt hoàn tất!")

if __name__ == "__main__":
    install_requirements()
    print("Chạy xong!")
