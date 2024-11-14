# generate_qr.py
import qrcode

def generate_qr(data, save_path):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to the specified path
    img.save(save_path)

if __name__ == "__main__":
    # Example usage: this can be tested independently
    data = "https://app.ecobarter.africa/rvm-api-endpoint?mn=eb6&pq=1&pw=2&cq=3&cw=4&tw=5&tp=6&si=sample-gid"
    generate_qr(data, "static/qrimages/info_qr.png")

