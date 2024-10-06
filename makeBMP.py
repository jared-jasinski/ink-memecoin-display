from PIL import Image, ImageDraw, ImageFont

def create_bmp(info):
    # BMP image size
    width, height = 400, 300
    
    # Create a new image with black background
    img = Image.new("RGB", (width, height), "black")
    draw = ImageDraw.Draw(img)
    
    # Extract the information
    try:
        name, current_price, percent_change, value_change = info.split(", ")
    except ValueError:
        print("Error: Incorrect format of input information.")
        return
    
    # Set font for text
    try:
        large_font = ImageFont.truetype("cour.ttf", 48)  # Further increased font size for name
        font = ImageFont.truetype("cour.ttf", 24)
    except IOError:
        large_font = ImageFont.load_default()
        font = ImageFont.load_default()
    
    # Draw a cool border
    border_width = 10
    draw.rectangle([border_width, border_width, width - border_width, height - border_width], outline="white", width=border_width)
    
    # Draw the name in a larger font, centered in the lower half of the top half of the image
    text_width, text_height = draw.textbbox((0, 0), name, font=large_font)[2:4]
    name_x = (width - text_width) / 2
    name_y = height / 2 - text_height - 10
    draw.text((name_x, name_y), f"{name}", fill="white", font=large_font)
    
    # Draw the current price, centered
    text_width, text_height = draw.textbbox((0, 0), current_price, font=large_font)[2:4]
    price_x = (width - text_width) / 2
    price_y = 150
    draw.text((price_x, price_y), f"{current_price}", fill="white", font=large_font)
    
    # Remove currency symbol for numeric comparison
    value_change_numeric = float(value_change.replace('$', ''))
    percent_change_numeric = float(percent_change.strip('%'))
    
    # Determine the arrow direction
    if percent_change_numeric >= 0 and value_change_numeric >= 0:
        arrow = "▲"  # Upward arrow
    else:
        arrow = "▼"  # Downward arrow
    
    # Draw the percent and value change, centered
    change_text = f" {arrow} {value_change} {percent_change}"
    text_width, text_height = draw.textbbox((0, 0), change_text, font=font)[2:4]
    change_x = (width - text_width) / 2
    change_y = price_y + 50
    draw.text((change_x, change_y), change_text, fill="white", font=font)
    
    # Save the image as BMP
    return img