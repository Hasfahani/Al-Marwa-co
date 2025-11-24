# AL MARWA CO - Professional Shipping & Forwarding Website

## Website Structure Overview

This is a professional, modern website for AL MARWA CO, a shipping and forwarding company, built using the Forty template from HTML5 UP.

### Pages Created

1. **index.html** - Homepage
   - Hero banner with company introduction
   - Service showcase with 6 key services
   - Call-to-action section
   - Contact information and footer

2. **about.html** - About Us Page
   - Company mission and vision
   - Core values (Reliability, Transparency, Expertise, Customer Focus)
   - Why choose AL MARWA CO
   - Complete list of capabilities
   - Links to services and contact

3. **services.html** - Services Page
   - Detailed descriptions of all 6 services:
     - Ocean Freight (FCL & LCL)
     - Air Freight
     - Customs Clearance & Documentation
     - Warehousing & Storage
     - Documentation & Compliance
     - Logistics Consultation
   - Call-to-action section
   - Quote request button

4. **contact.html** - Contact Page
   - Contact information (email, phone, address, hours)
   - Contact form with fields for:
     - Name, Email, Company, Phone
     - Service selection dropdown
     - Shipment origin and destination
     - Message/Details textarea
   - Why businesses trust AL MARWA CO section
   - Responsive contact details

### Folder Structure

```
al marwaco/
├── index.html
├── about.html
├── services.html
├── contact.html
├── assets/
│   ├── css/
│   │   ├── main.css
│   │   ├── noscript.css
│   │   └── (other CSS files)
│   ├── js/
│   │   ├── jquery.min.js
│   │   ├── jquery.scrolly.min.js
│   │   ├── jquery.scrollex.min.js
│   │   ├── browser.min.js
│   │   ├── breakpoints.min.js
│   │   ├── util.js
│   │   └── main.js
│   ├── images/
│   │   ├── ocean-freight.jpg
│   │   ├── air-freight.jpg
│   │   ├── customs.jpg
│   │   ├── warehousing.jpg
│   │   ├── documentation.jpg
│   │   ├── consultation.jpg
│   │   └── README.txt
│   ├── sass/
│   │   └── (SCSS files for customization)
│   └── webfonts/
├── README.txt (original template)
└── LICENSE.txt

```

### Key Features

✅ **Responsive Design**
- Mobile-first approach using HTML5UP Forty template
- Adapts to all screen sizes (mobile, tablet, desktop)
- Touch-friendly navigation

✅ **Professional Navigation**
- Responsive navbar with hamburger menu on mobile
- Consistent menu across all pages
- Easy navigation between sections

✅ **Service Showcase**
- Grid layout of 6 key services with images
- Individual service detail pages with full descriptions
- Anchor links for easy navigation within pages

✅ **Contact & Forms**
- Comprehensive contact form with validation
- Contact information sections with icons
- Business hours display
- Multiple contact methods (email, phone, address)

✅ **Modern & Clean Design**
- Professional color scheme suitable for logistics
- Clear typography and spacing
- Whitespace for better readability
- Call-to-action buttons throughout

✅ **SEO Optimized**
- Proper HTML5 structure
- Semantic markup
- Meta tags and titles on each page
- Descriptive alt text for images

### CSS & JavaScript

**CSS Files** (assets/css/)
- `main.css` - Main stylesheet with responsive grid, components, and layouts
- `noscript.css` - Fallback styles for browsers without JavaScript

**JavaScript Files** (assets/js/)
- `jquery.min.js` - jQuery library
- `jquery.scrolly.min.js` - Smooth scrolling plugin
- `jquery.scrollex.min.js` - Scroll effects plugin
- `browser.min.js` - Browser detection
- `breakpoints.min.js` - Responsive breakpoint handling
- `util.js` - Utility functions
- `main.js` - Main functionality and interactions

### Customization Guide

#### Colors & Branding
- Edit `assets/sass/libs/_vars.scss` for color variables
- Update company name in header and footer across all pages
- Add company logo if needed

#### Contact Information
- Update email: `info@almarwaco.com`
- Add actual phone number
- Insert real address and business hours
- Update social media links in footer

#### Images
- Add actual shipping/logistics images to `assets/images/`
- Image names: ocean-freight.jpg, air-freight.jpg, customs.jpg, warehousing.jpg, documentation.jpg, consultation.jpg
- Recommended size: 1200x600px (or 800x400px minimum)
- Ensure images are optimized for web

#### Content
- Replace placeholder text with real company content
- Add actual service descriptions
- Update about section with company history
- Customize mission and vision statements

#### Services
- Modify service names and descriptions as needed
- Add or remove service sections
- Update pricing (if applicable)

#### Forms
- Configure form submission endpoint in `contact.html`
- Update form action attribute from `#` to actual form handler URL
- Consider using services like Formspree, Netlify Forms, or custom backend

### Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

### Performance Optimization Tips

1. **Image Optimization**
   - Compress images without quality loss
   - Use appropriate formats (JPG for photos, PNG for graphics)
   - Consider lazy loading for images below the fold

2. **Caching**
   - Enable browser caching for static assets
   - Use CDN for faster delivery

3. **Minification**
   - CSS and JavaScript are already minified
   - Use build tools for additional optimization

### Getting Started

1. **View the website:**
   - Open any HTML file in a web browser
   - Or use a local server: `python -m http.server` (Python 3)

2. **Customize content:**
   - Edit text in each HTML file
   - Add real company information
   - Insert actual images

3. **Deploy:**
   - Upload to web hosting
   - Use services like Vercel, Netlify, or GitHub Pages
   - Ensure all assets paths are correct

### Support & Credits

- **Template:** Forty by HTML5 UP
- **License:** Creative Commons 3.0 License (html5up.net/license)
- **Built with:** HTML5, CSS3, jQuery

### Future Enhancements

- Blog section for industry news and tips
- Client testimonials carousel
- Service pricing tables
- Live chat support
- Tracking system integration
- Multi-language support
- Online booking system
- Customer login portal

---

**Last Updated:** November 2025
**Version:** 1.0
**Status:** Ready for Customization
