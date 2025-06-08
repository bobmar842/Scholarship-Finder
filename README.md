# 🎓 ScholarScope

## 🧩 Problem Statement

Finding scholarships is often a time-consuming and confusing task for students. Opportunities are spread across multiple platforms, each with its own eligibility rules, deadlines, and vague application steps. The Scholarship Finder tool is designed to streamline and automate this process, helping students uncover scholarships that closely align with their academic background, location, and personal criteria.

---

## 🎯 Goals

-Automatically scrape and compile scholarships from several trusted sources.
-Allow students to create a personalized profile (course, GPA, region, etc.) to receive filtered results.
-Implement a smart matching algorithm to rank scholarships based on relevance and urgency.
-Offer a clean, intuitive UI for browsing, filtering, and applying to scholarships.

---

## ⚙️ Tech Stack / Frameworks Used

| Layer        | Tools / Frameworks |
|--------------|--------------------|
| Frontend     | HTML, CSS, React.js |
| Backend      | Node.js, Express.js / FastAPI |
| Scraping     | BeautifulSoup, Scrapy |
| Sentiment Analysis | TextBlob, VADER |
| Database     | MongoDB |

---

## 🚀 Features

### 🔐 Student Profile Section
- Input fields for:
  - Course of study
  - GPA / Grades
  - Location
  - Optional: Income status, Special categories (minority, disability, etc.)

### 🕸️ Web Scraping Sources
- Major platforms like:
  - Chegg
  - Scholarships.com
  - Fastweb
- University-specific portals
- Niche platforms for demographic or field-specific opportunities

### 🧠 Scholarship Categorization & Matching
- Attributes:
  - **Amount**: Full / Partial / Small Grants
  - **Eligibility**: Based on course, GPA, region, income, etc.
  - **Deadline**: Filter by urgency (notifications for upcoming ones)

### 📄 Personalized Scholarship List
- Ranks scholarships by:
  - Profile relevance
  - Deadline urgency
  - Scholarship amount
- Each entry includes:
  - Eligibility summary
  - Application deadline
  - Award amount
  - Direct application link
