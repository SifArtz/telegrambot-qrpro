import requests

def create_qrcode_from_link(link):
    url = "https://qrcode3.p.rapidapi.com/qrcode/text"

    payload = {
    	"data": link,
    	"image": {
    		"uri": "https://psv4.userapi.com/c909518/u215425679/docs/d21/af546d6ed380/idq5pKWoKI_1711838584060_waifu2x_noise3_scale4x-round-corners_1.png?extra=w8zGcKr8MP-0XD3ZNePTcAFkRw2YMuv__Ejqxl2w6sQZ2h67trR6Igrz6NAekVC0FPN1xsQ50xdamprWiCITHQPEUhwsYR0uuNj7CAJFKw5bAaAzQFM6DOu4OwP86xp09taH3rm1vHD0VaI5mODJMwBgYQ",
    		"modules": True
    	},
    	"style": {
    		"background": { "color": "#FFFFFF" },
    		"module": {
    			"shape": "heavyround",
    			"color": "#008A97"
    		},
    		"inner_eye": {
    			"shape": "heavyround",
    			"color": "#489EAB"
    		},
    		"outer_eye": {
    			"shape": "heavyround",
    			"color": "#585858"
    		}
    	},
    	"size": {
    		"width": 650,
    		"quiet_zone": 4,
    		"error_correction": "M"
    	},
    	"output": {
    		"filename": "qrcode",
    		"format": "png"
    	}
    }
    headers = {
    	"content-type": "application/json",
    	"X-RapidAPI-Key": "40f0f34803mshc45ce1054770be1p14d741jsn8cdd3830bbc9",
    	"X-RapidAPI-Host": "qrcode3.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response)
    with open("qrcode.png", "wb") as f:
        f.write(response.content)

    print("QR-код сохранен в файле 'qrcode.png'")

