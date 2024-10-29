# This Python file uses the following encoding: utf-8
from escpos.printer import Usb
import uuid


p = Usb(0x0483, 0x5743, in_ep=0x82, out_ep=0x01, profile="TM-T88III")
from time import *
from datetime import date
import qrcode
from datetime import datetime
now = datetime.now()
dt_string = now.strftime("  %b/%d/%Y     %H:%M:%S")
#print("Today's date:", dt_string)
def print_it(Tw,Tp,Cw,Bw,Cc,Bc,gid):
	
	#gid = uuid.uuid4().hex


	data = f"https://app.ecobarter.africa/rvm-api-endpoint?mn=eb6&pq={Bc}&pw={Bw}&cq={Cc}&cw={Cw}&tw={Tw}&tp={Tp}&si={gid}"

	# Combine all the information into a single string separated by a delimiter
	#combined_data = "\n".join(data)

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

	# Save the image
	img.save("static/qrimages/info_qr.png")
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
	#Printing the image
	p.image("static/image/ECO2.png",impl="bitImageColumn")
	#printing the initial data
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
	p.image("static/qrimages/info_qr.png",impl="bitImageColumn")
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
	#p.textln(f"Total PT            {Tp} Pt")
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
	p.textln("===========================")
	p.textln("QTY       ITEM         WT")
	p.textln("--------------------------")
	p.textln(f"{Bc}      Pet Bottle     {Bw}g")
	p.textln(f"{Cc}     Beverage Can   {Cw}g")
	p.textln("--------------------------")
	p.textln(f"{Cc+Bc}                    {Tw}g")
	p.textln("--------------------------")
	p.textln("         THANK YOU        ")
	p.textln("==========================")
	p.textln("\n")
	p.textln("Recycle more         Earn more")
	p.textln("\n")
	p.textln("  Scan to claim on the app")
	p.textln("             or           ")
	p.textln("  Visit our nearest partner store")
	p.cut()
#if your printer has paper cuting facility then you can use this function
#print("done")
if __name__ == "__main__":
    print_it(1,2,3,4,5,6)
