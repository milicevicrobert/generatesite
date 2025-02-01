import streamlit as st
from jinja2 import Template

# HTML Template with Jinja2
html_template = """
<!DOCTYPE html>
<html lang="hr">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta
            name="description"
            content="{{ company.name }} - Company information, contact details, and more." />
        <meta name="keywords" content="{{ company.name }}, company, Zagreb, Croatia, contact" />
        <title>{{ company.name }}</title>
        <link rel="icon" type="image/x-icon" href="favicon.ico" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
        <style>
            :root {
                --random-bg-color: darkviolet;

                --glow-color: white;
            }

            body {
                margin: 0;
                padding: 0;
                background: var(--random-bg-color);
                background-size: cover;
                background-position: center;
                color: white;
                font-family: 'Arial', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                overflow: hidden;
                position: relative;
            }
            .background-anim {
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                pointer-events: none;
                z-index: -1;
            }

            .container {
                width: 80%;
                max-width: 500px;
                padding: 20px;
                border-radius: 10px;
                background: rgba(0, 0, 0, 0.7);
                box-shadow: 10px 10px 50px var(--glow-color);
                transform: scale(0);
                text-align: left;
            }

            .bubble {
                position: absolute;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 50%;
                filter: blur(2px);
                opacity: 0.6;
            }

            h1 {
                font-size: 3rem;
                padding: 10%;
                margin: 0 0 20px;
                text-align: center;
                color: var(--glow-color);
                text-shadow: 0 0 0 var(--glow-color), 0px 0px 20px var(--glow-color);
            }

            .info {
                font-size: 1.3rem;
                line-height: 2;
                color: white;
            }

            .info p {
                opacity: 0;
                margin: 5px 0;
            }

            a {
                color: var(--glow-color);
                text-decoration: underline;
            }

            .copy-button {
                margin-top: 40px;
                padding: 10px 20px;
                background-color: var(--random-bg-color);
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1rem;
                transition: background-color 0.3s ease, transform 0.3s ease;
            }

            .copy-button:hover {
                background-color: var(--glow-color);
                transform: scale(1.1);
            }

            @media (max-width: 600px) {
                h1 {
                    font-size: 2rem;
                }
                .info {
                    font-size: 0.9rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="background-anim" id="background"></div>

        <div class="container" id="container">
            <h1 id="title">{{ company.name }}</h1>
            <div class="info" id="info">
                <p id="line1">Adresa: {{ company.address }}</p>
                <p id="line2">OIB: {{ company.oib }}</p>
                <p id="line3">MB: 04379918</p>
                <p id="line4">MBS: 080965808</p>
                <p id="line5">IBAN: {{ company.iban }}</p>
                <p id="line6">Direktor: {{ company.director }}</p>
                <p id="line7">
                    Web:
                    <a href="https://{{ company.website }}" aria-label="Visit {{ company.name }}">
                        {{ company.website }}
                    </a>
                </p>
                <p id="line8">
                    Email:
                    <a href="mailto:{{ company.email }}" aria-label="Email {{ company.name }}">
                        {{ company.email }}
                    </a>
                </p>
            </div>
            <button class="copy-button" id="copyButton">i</button>
        </div>
        <!-- Dodajemo kontejner za notifikacije -->
        <div
            id="notification-container"
            style="position: fixed; bottom: 20px; right: 20px; z-index: 1000"></div>

        <script>
            // Generiraj slučajnu boju
            function getRandomColor() {
                const letters = '0123456789ABCDEF';
                let color = '#';
                for (let i = 0; i < 6; i++) {
                    color += letters[Math.floor(Math.random() * 16)];
                }
                return color;
            }

            // Generiraj "glow" boju
            function getGlowColor(hex) {
                hex = hex.replace(/^#/, '');
                let r = parseInt(hex.substring(0, 2), 16);
                let g = parseInt(hex.substring(2, 4), 16);
                let b = parseInt(hex.substring(4, 6), 16);
                let hsl = rgbToHsl(r, g, b);
                hsl[2] = Math.min(0.8, hsl[2] + 0.3);
                let glowRgb = hslToRgb(hsl[0], hsl[1], hsl[2]);
                return `#${glowRgb[0].toString(16).padStart(2, '0')}${glowRgb[1]
                    .toString(16)
                    .padStart(2, '0')}${glowRgb[2].toString(16).padStart(2, '0')}`;
            }

            // RGB u HSL
            function rgbToHsl(r, g, b) {
                (r /= 255), (g /= 255), (b /= 255);
                let max = Math.max(r, g, b),
                    min = Math.min(r, g, b);
                let h,
                    s,
                    l = (max + min) / 2;
                if (max === min) {
                    h = s = 0;
                } else {
                    let d = max - min;
                    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
                    switch (max) {
                        case r:
                            h = (g - b) / d + (g < b ? 6 : 0);
                            break;
                        case g:
                            h = (b - r) / d + 2;
                            break;
                        case b:
                            h = (r - g) / d + 4;
                            break;
                    }
                    h /= 6;
                }
                return [h, s, l];
            }

            // HSL u RGB
            function hslToRgb(h, s, l) {
                let r, g, b;
                if (s === 0) {
                    r = g = b = l;
                } else {
                    function hue2rgb(p, q, t) {
                        if (t < 0) t += 1;
                        if (t > 1) t -= 1;
                        if (t < 1 / 6) return p + (q - p) * 6 * t;
                        if (t < 1 / 2) return q;
                        if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
                        return p;
                    }
                    let q = l < 0.5 ? l * (1 + s) : l + s - l * s;
                    let p = 2 * l - q;
                    r = hue2rgb(p, q, h + 1 / 3);
                    g = hue2rgb(p, q, h);
                    b = hue2rgb(p, q, h - 1 / 3);
                }
                return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
            }

            // Postavi slučajne boje
            const rnd_bg_col = getRandomColor();

            const glow_col = getGlowColor(rnd_bg_col);
            document.documentElement.style.setProperty('--random-bg-color', rnd_bg_col);

            document.documentElement.style.setProperty('--glow-color', glow_col);

            // GSAP animacija pozadine
            gsap.to('body', {
                '--random-bg-color': 'hsl(280, 80%, 40%)', // Nova boja u HSL formatu
                duration: 30, // Duža animacija za suptilan efekt
                repeat: -1,
                yoyo: true,
                ease: 'sine.inOut'
            });

            gsap.fromTo(
                '#container',
                { scale: 0, opacity: 0 },
                { scale: 1, opacity: 1, duration: 1.5, ease: 'bounce' }
            );

            gsap.to('#title', {
                scale: 1.05,
                duration: 5,
                repeat: -1,
                yoyo: true,
                ease: 'sine.inOut'
            });

            gsap.fromTo(
                '.info p',
                { opacity: 0, y: 10 },
                {
                    opacity: 1,
                    y: 0,
                    duration: 1.5,
                    stagger: 1,
                    ease: 'power2.out'
                }
            );

            function createBubble() {
                let bubble = document.createElement('div');
                bubble.classList.add('bubble');
                document.getElementById('background').appendChild(bubble);

                let size = Math.random() * 100 + 20;
                bubble.style.width = `${size}px`;
                bubble.style.height = `${size}px`;
                bubble.style.left = `${Math.random() * 100}vw`;
                bubble.style.bottom = '-10vh';

                gsap.to(bubble, {
                    y: '-120vh',
                    opacity: 0,
                    duration: Math.random() * 5 + 3,
                    ease: 'sine.out',
                    onComplete: () => bubble.remove()
                });
            }

            setInterval(createBubble, 500);

            // Funkcija za prikaz obavijesti s animacijom
            function showNotification(message) {
                const container = document.getElementById('notification-container');

                let notification = document.createElement('div');
                notification.textContent = message;

                // Stilizacija notifikacije
                notification.style.background = 'rgba(50, 50, 50, 0.9)';
                notification.style.color = 'white';
                notification.style.padding = '12px 20px';
                notification.style.borderRadius = '8px';
                notification.style.fontSize = '14px';
                notification.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
                notification.style.opacity = '0';
                notification.style.transition =
                    'opacity 0.3s ease-in-out, transform 0.3s ease-in-out';
                notification.style.marginBottom = '10px';
                notification.style.transform = 'translateY(-10px)';
                notification.style.display = 'inline-block';

                container.appendChild(notification);

                // Animacija pojavljivanja
                requestAnimationFrame(() => {
                    notification.style.opacity = '1';
                    notification.style.transform = 'translateY(0)';
                });

                // Nestajanje nakon 3 sekunde
                setTimeout(() => {
                    notification.style.opacity = '0';

                    notification.style.transform = 'translateY(-10px)';
                    setTimeout(() => notification.remove(), 500);
                }, 3000);
            }

            // Kopiranje podataka u međuspremnik s poboljšanom notifikacijom
            document.getElementById('copyButton').addEventListener('click', function () {
                const companyData = `{{ company.name }}\nAdresa: {{ company.address }}\nOIB: {{ company.oib }}\nemail: {{ company.email }}\nIBAN: {{ company.iban }}`;

                navigator.clipboard
                    .writeText(companyData.trim())
                    .then(() => {
                        showNotification('✅ Podaci su kopirani u međuspremnik!');
                    })
                    .catch(() => {
                        showNotification('❌ Greška pri kopiranju. Pokušajte ponovno.');
                    });
            });
        </script>
    </body>
</html>

"""

# Streamlit UI
def main():
    st.title("Generiranje HTML stranice o firmi")
    
    # Unos podataka
    company_name = st.text_input("Naziv firme", "Neki novi d.o.o.")
    address = st.text_input("Adresa", "Cebini 28, 10010 Zagreb, Hrvatska")
    oib = st.text_input("OIB", "13544383037")
    iban = st.text_input("IBAN", "HR92 2500009 123456789")
    director = st.text_input("Direktor", "Pero Perić")
    website = st.text_input("Web stranica https:// ", "www.conectmarketplace.hr")
    email = st.text_input("Email", "pero@connectmarketplace.hr")
    
    if st.button("Generiraj HTML"):
        # Kreiranje Jinja2 templatea
        template = Template(html_template)
        
        company_data = {
            "name": company_name,
            "address": address,
            "oib": oib,
            "iban": iban,
            "director": director,
            "website": website,
            "email": email
        }
        
        # Generiranje HTML sadržaja
        html_output = template.render(company=company_data)
        
        # Kreiranje imena fajla
        filename = f"{company_name.replace(' ', '_').lower()}_index.html"
        
        # Spremanje HTML-a
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_output)
        
        st.success(f"HTML generiran i spremljen kao `{filename}`")
        
        # Prikaz generiranog HTML-a
        st.download_button(
            label="Preuzmi HTML",
            data=html_output,
            file_name=filename,
            mime="text/html"
        )

if __name__ == "__main__":
    main()
