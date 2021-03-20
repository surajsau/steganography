from PIL import Image

def encode(src, message, dest):
    img = Image.open(src, 'r')

    px_img = img.load()

    if img.mode == "RGB":
        channels = 3
    elif img.mode == "RGBA":
        channels = 4

    message += "$$$$" ## limiter to check end of string

    message_bytes = ''.join(['{0:08b}'.format(ord(message[i])) for i in range(len(message))])

    new_image = Image.new(img.mode, img.size)
    px_new = new_image.load()

    message_index = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            hidden_px = [0] * channels

            for k in range(channels):
                px = px_img[i, j][k]
                px_bin = '{0:08b}'.format(px)

                if message_index < len(message_bytes):
                    hidden_px[k] = int(px_bin[:7] + message_bytes[message_index], 2)
                    message_index += 1
                else:
                    hidden_px[k] = int(px_bin, 2)
            px_new[i, j] = tuple(hidden_px)

            # if message_index < len(message_bytes):
            #     message_bits = ()
            #     h_r, h_g, h_b, h_a = (rgba[0][:7] + message_bytes[message_index][0], 
            #         rgba[1][:7] + message_bytes[message_index][1], 
            #         rgba[2][:7] + message_bytes[message_index][2], 
            #         rgba[3][:7] + message_bytes[message_index][3])
            #     message_index += 1
            # else:
            #     h_r, h_g, h_b, h_a = rgba
            # px_new[i, j] = (int(h_r, 2), int(h_g, 2), int(h_b, 2), int(h_a, 2))

    new_image.save(dest)

def decode(src):
    img = Image.open(src, 'r')

    px_img = img.load()

    if img.mode == "RGB":
        channels = 3
    elif img.mode == "RGBA":
        channels = 4

    hidden_bits = ""
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            for k in range(channels):
                px = px_img[i, j][k]
                px_bin = '{0:08b}'.format(px)

                hidden_bits += px_bin[-1]
            # r, g, b, a = px_img[i, j]
            # rgba = ('{0:08b}'.format(r),'{0:08b}'.format(g),'{0:08b}'.format(b),'{0:08b}'.format(a))

            # hidden_bits += "" + rgba[0][-1] + rgba[1][-1] + rgba[2][-1] + rgba[3][-1]

    hidden_bytes = [hidden_bits[i: i+8] for i in range(0, len(hidden_bits), 8)]

    hidden_message = ""
    for i in range(len(hidden_bytes)):
        if hidden_message[-4:] == "$$$$":
            break
        else:
            hidden_message += chr(int(hidden_bytes[i], 2))

    if "$$$$" in hidden_message:
        print(hidden_message[:-4])
    else:
        print("No hidden message found ", hidden_message[:10])


def main():
    print('encode or decode?')
    print('1 for encode')
    print('2 for decode')
    function_type = input()

    if function_type == "1":
        print('img: ')
        img = input()
        print('message: ')
        message = input()
        print('dest: ')
        dest = input()

        encode(img, message, dest)
    elif function_type == "2":
        print('src: ')
        src = input()
        decode(src)
    else:
        print('invalid input')
        main()

if __name__ == "__main__":
    main()