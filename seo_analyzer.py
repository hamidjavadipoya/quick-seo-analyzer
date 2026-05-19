import requests
from bs4 import BeautifulSoup
import sys

def analyze_seo(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    print(f"🔍 Analyzing Technical SEO for: {url}")
    print("="*50)
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Title Tag Audit
        title = soup.find('title')
        if title and title.text.strip():
            print(f"✅ Title Tag: '{title.text.strip()}' ({len(title.text.strip())} characters)")
        else:
            print("❌ Meta Title: Missing or empty tag!")
            
        # 2. Meta Description Audit
        description = soup.find('meta', attrs={'name': 'description'})
        if description and description.get('content', '').strip():
            desc_text = description['content'].strip()
            print(f"✅ Meta Description: '{desc_text[:60]}...' ({len(desc_text)} characters)")
        else:
            print("❌ Meta Description: Missing attribute!")
            
        # 3. Headings Hierarchy Audit
        h1s = soup.find_all('h1')
        print(f"📊 Heading H1 Count: {len(h1s)}")
        for idx, h1 in enumerate(h1s, 1):
            print(f"   -> H1 [{idx}]: {h1.text.strip()[:50]}")
        if len(h1s) == 0:
            print("⚠️ Warning: Missing H1 tag! Critical for semantic structure.")
        elif len(h1s) > 1:
            print("⚠️ Warning: Multiple H1 tags detected. Best practice recommends exactly one H1 per page.")
            
        # 4. Images Alt Attributes Audit
        images = soup.find_all('img')
        missing_alt = sum(1 for img in images if not img.get('alt'))
        print(f"🖼️ Total Images Found: {len(images)}")
        if missing_alt > 0:
            print(f"⚠️ Warning: {missing_alt} image(s) are missing the crucial 'alt' attribute.")
        else:
            print("✅ Perfect: All images have alternative text defined.")
            
    except Exception as e:
        print(f"❌ Error fetching or parsing the targeted URL: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        analyze_seo(target)
    else:
        print("Usage: python seo_analyzer.py <url>")
