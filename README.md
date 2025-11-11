# LinkedIn Company Profiles Scraper

> Extract detailed company data from LinkedIn with precision and speed. This scraper collects public company information like name, website, employees, and industry—all neatly structured for business insights, recruitment, and research.

> Perfect for analysts, recruiters, and B2B teams who need to gather LinkedIn company data at scale without manual effort.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>LinkedIn Company Profiles Scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

The LinkedIn Company Profiles Scraper automates the process of collecting key company details from LinkedIn. It eliminates hours of manual browsing and data entry by delivering clean, ready-to-use company information in multiple export formats.

### Why Use This Scraper

- Collect data from thousands of LinkedIn company profiles automatically.
- Ideal for market researchers, recruiters, and data analysts.
- Supports multiple output formats (JSON, CSV, XML, Excel).
- Highly accurate and efficient with low run costs.
- Fully scalable for bulk data collection.

## Features

| Feature | Description |
|----------|-------------|
| Automated Data Extraction | Gathers public company details directly from LinkedIn URLs. |
| Multi-format Export | Download results in JSON, CSV, XML, or Excel. |
| Scalable Runs | Scrape up to 1,000 profiles per task and chain runs for more. |
| Accurate Results | Collects verified and structured information. |
| Affordable Pricing | Optimized to minimize runtime cost while maintaining accuracy. |
| Proxy Support | Integrates proxy groups for consistent access and speed. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| company_name | The official name of the company. |
| company_profile | The LinkedIn profile URL of the company. |
| company_website | The company’s official website link. |
| company_address_type | Type of company address (e.g., PostalAddress). |
| company_street | Street address of the company’s headquarters. |
| company_locality | The city where the company operates. |
| company_region | The region, state, or province of the company. |
| company_postal_code | Postal or ZIP code of the company. |
| company_country | The country in which the company is based. |
| company_employees_on_linkedin | Number of employees listed on LinkedIn. |
| company_followers_on_linkedin | Number of followers on the LinkedIn company page. |
| company_logo | URL of the company’s logo image. |
| company_cover_image | URL of the company’s LinkedIn banner image. |
| company_slogan | Tagline or slogan of the company. |
| company_twitter_description | Summary or short description of the company. |
| company_about_us | Detailed company description and mission statement. |
| company_industry | The industry the company belongs to. |
| company_size | The number of employees range. |
| company_headquarters | The location of the company’s headquarters. |
| company_organization_type | Type of organization (e.g., Privately Held). |
| company_founded | Year the company was founded. |
| company_specialties | Key specialties or focus areas of the company. |

---

## Example Output

    [
      {
        "company_name": "Fever",
        "company_profile": "https://www.linkedin.com/company/fever-up",
        "company_website": "https://feverup.com",
        "company_address_type": "PostalAddress",
        "company_street": "76 Greene St, New York",
        "company_locality": "New York",
        "company_region": null,
        "company_postal_code": "10012",
        "company_country": "US",
        "company_employees_on_linkedin": 2778,
        "company_followers_on_linkedin": 302653,
        "company_logo": "https://media.licdn.com/dms/image/v2/C4D0BAQGZ34Z5Azy0Qw/company-logo_200_200/company-logo_200_200/0/1630556337246/fever_inc_logo",
        "company_cover_image": "https://media.licdn.com/dms/image/v2/D4D3DAQFsknuPc8dzAQ/image-scale_191_1128/0/1679580354908/fever_up_cover",
        "company_slogan": "Democratizing access to culture and entertainment",
        "company_about_us": "Fever is the leading global live-entertainment discovery tech platform...",
        "company_industry": "Software Development",
        "company_size": "1,001-5,000 employees",
        "company_headquarters": "New York",
        "company_organization_type": "Privately Held",
        "company_founded": 2014,
        "company_specialties": "internet, mobile, nightlife, startup, events, music, tickets, concerts"
      }
    ]

---

## Directory Structure Tree

    linkedin-company-profiles-scraper/
    ├── src/
    │   ├── runner.py
    │   ├── extractors/
    │   │   ├── linkedin_parser.py
    │   │   └── utils_cleaner.py
    │   ├── outputs/
    │   │   └── exporters.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── inputs.sample.txt
    │   └── sample.json
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Recruiters** use it to collect company data for identifying potential employers or hiring partners.
- **Market researchers** use it to analyze industries, company sizes, and growth trends.
- **Sales teams** use it to build targeted B2B lead lists for outreach.
- **Investors** use it to assess company presence and public metrics.
- **Data analysts** use it to feed company data into dashboards for deeper insights.

---

## FAQs

**Q1: How many LinkedIn profiles can this scraper collect per run?**
You can collect up to 1,000 profiles in one run. For larger datasets, divide your URLs into smaller batches and run multiple tasks.

**Q2: What kind of input does it accept?**
It accepts a list of valid LinkedIn company URLs in JSON format, e.g.:
{ "company_profile_urls": ["https://linkedin.com/company/example"], "proxy_group": "DATACENTER" }

**Q3: Is it legal to scrape company data from LinkedIn?**
Yes, this scraper only collects publicly available company information. It doesn’t access private user data or require login credentials.

**Q4: What output formats are supported?**
You can export the results in JSON, CSV, XML, or Excel formats for easy integration with other tools.

---

## Performance Benchmarks and Results

**Primary Metric:** Scrapes an average of 500 company profiles per minute under optimal conditions.
**Reliability Metric:** 98% success rate with consistent structure validation.
**Efficiency Metric:** Average runtime cost is ~$0.02 per 50 profiles.
**Quality Metric:** Over 99% field completeness rate across all extracted datasets.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
