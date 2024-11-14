# print_receipt.py
from escpos.printer import Usb
from time import sleep
from datetime import datetime
from createqr import generate_qr

# Printer initialization
p = Usb(0x0483, 0x5743, in_ep=0x82, out_ep=0x01, profile="TM-T88III")

now = datetime.now()
dt_string = now.strftime("  %b/%d/%Y     %H:%M:%S")

def print_it(Tw, Tp, Cw, Bw, Cc, Bc, gid):
    # Prepare the URL for the QR code
    data = f"https://app.ecobarter.africa/rvm-api-endpoint?mn=eb6&pq={Bc}&pw={Bw}&cq={Cc}&cw={Cw}&tw={Tw}&tp={Tp}&si={gid}"

    # Generate and save the QR code image
    generate_qr(data, "static/qrimages/info_qr.png")

    # Start printing
    p.set(
        underline=0,
        align="center",
        font="a",
        width=2,
        height=2,
        density=8,
        invert=0,
        smooth=False,
        flip=False,
    )
    
    # Print the initial logo
    p.image("static/image/ECO2.png", impl="bitImageColumn")
    
    # Print the QR code
    p.set(
        underline=0,
        align="center",
        font="a",
        width=2,
        height=2,
        density=2,
        invert=0,
        smooth=False,
        flip=False,
    )
    p.image("static/qrimages/info_qr.png", impl="bitImageColumn")

    # Print the receipt text
    p.textln("")
    p.set(
        underline=0,
        align="center",
        font="a",
        width=2,
        height=2,
        density=2,
        invert=0,
        smooth=False,
        flip=False,
    )
    p.textln("--------------------------")
    p.textln(dt_string)
    p.textln("\n")
    
    # Print details
    p.set(
        underline=0,
        align="center",
        font="a",
        bold=True,
        width=2,
        height=2,
        density=2,
        invert=0,
        smooth=False,
        flip=False,
    )
    p.textln("===========================")
    p.textln("QTY       ITEM         WT")
    p.textln("--------------------------")
    p.textln(f"{Bc}      Pet Bottle     {Bw}g")
    p.textln(f"{Cc}     Beverage Can   {Cw}g")
    p.textln("--------------------------")
    p.textln(f"{Cc + Bc}                    {Tw}g")
    p.textln("--------------------------")
    p.textln("         THANK YOU        ")
    p.textln("==========================")
    p.textln("\n")
    p.textln("Recycle more         Earn more")
    p.textln("\n")
    p.textln("  Scan to claim on the app")
    p.textln("             or           ")
    p.textln("  Visit our nearest partner store")
    
    # Cut paper (if printer supports this feature)
    p.cut()

if __name__ == "__main__":
    # Sample call to print_it function
    print_it(1, 2, 3, 4, 5, 6, "sample-gid")

