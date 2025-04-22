import os
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the URL of the visual set list
BASE_URL = 'https://www.justinbasil.com/visual/sv9'

# Create directories for images and output
os.makedirs('images', exist_ok=True)

# Initialize the CSV file
with open('journey_together_ebay.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow([
        'Action', 'Title', 'Category', 'Condition', 'Format',
        'Relationship', 'RelationshipDetails', 'CustomLabel',
        'Quantity', 'StartPrice', 'PictureURL', 'Holo'
    ])

    # Add the parent listing row
    writer.writerow([
        'Add', 'Pokémon TCG: Journey Together - Choose Your Card',
        '183454', 'Used', 'FixedPrice', '', '', '', '', '', '', ''
    ])

    # Fetch the visual set list page
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    for img in img_tags:
        img_url = img.get('src')
        if not img_url:
            continue
        # Construct the full image URL
        full_img_url = urljoin(BASE_URL, img_url)
        # Extract the filename from the URL
        filename = os.path.basename(img_url)
        # Extract card number from filename (assuming format '001.jpg', '002.jpg', etc.)
        card_number = os.path.splitext(filename)[0]
        # Define the local path to save the image
        image_path = os.path.join('images', f'{card_number}-front.jpg')
        # Download and save the image
        img_data = requests.get(full_img_url).content
        with open(image_path, 'wb') as handler:
            handler.write(img_data)
        # Determine Holo status (this may require additional logic or data)
        holo_status = 'Non-Holo'  # Placeholder; implement logic to determine actual status
        # Write the variation row to the CSV
        writer.writerow([
            '', '', '', '', '', 'Variation',
            f'Card={card_number}', card_number,
            '1', '1.00', image_path, holo_status
        ])
