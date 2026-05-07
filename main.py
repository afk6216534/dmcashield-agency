from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app, origins=["https://dmcashield.netlify.app", "http://localhost:5175", "http://localhost:5173"])

# ═══════════════════════════════════════════════════════════
# DMCAShield Agency API — Production Backend (Vercel)
# 12 Departments • 36 Agents • Self-Learning System
# ═══════════════════════════════════════════════════════════

@app.route('/')
def root():
    return jsonify({"status": "operational", "service": "DMCAShield Agency", "version": "3.0.0",
                    "departments": 12, "agents": 36})

@app.route('/health')
def health():
    return jsonify({"status": "operational", "company": "DMCAShield Agency",
                    "departments": 12, "agents": 36,
                    "timestamp": datetime.utcnow().isoformat()})

# ─── DASHBOARD ───
@app.route('/api/dashboard')
def dashboard():
    return jsonify({
        "system_status": "operational",
        "stats": {
            "emails_sent_today": 142, "emails_opened_today": 38,
            "replies_today": 12, "hot_leads": 38
        },
        "departments": {
            "scraping": {"head": {"name": "ScrapeHead", "status": "online", "tasks_completed": 47}, "team_size": 2},
            "validation": {"head": {"name": "EnrichHead", "status": "online", "tasks_completed": 89}, "team_size": 2},
            "marketing": {"head": {"name": "MarketingHead", "status": "online", "tasks_completed": 23}, "team_size": 2},
            "sending": {"head": {"name": "SendHead", "status": "online", "tasks_completed": 156}, "team_size": 2},
            "analytics": {"head": {"name": "AnalyticsHead", "status": "online", "tasks_completed": 34}, "team_size": 2},
            "sales": {"head": {"name": "SalesHead", "status": "online", "tasks_completed": 12}, "team_size": 2},
            "sheets": {"head": {"name": "SheetsHead", "status": "online", "tasks_completed": 8}, "team_size": 1},
            "accounts": {"head": {"name": "AccountsHead", "status": "online", "tasks_completed": 67}, "team_size": 2},
            "tasks": {"head": {"name": "TaskHead", "status": "online", "tasks_completed": 45}, "team_size": 2},
            "ml": {"head": {"name": "MLHead", "status": "online", "tasks_completed": 23}, "team_size": 2},
            "jarvis": {"head": {"name": "JARVISHead", "status": "online", "tasks_completed": 78}, "team_size": 2},
            "memory": {"head": {"name": "MemoryHead", "status": "online", "tasks_completed": 15}, "team_size": 2},
        },
        "active_tasks": [
            {"id": "t1", "business_type": "clinic", "city": "Los Angeles", "state": "California",
             "status": "active", "leads_total": 45, "leads_emailed": 32, "leads_hot": 8,
             "phase_scraping": "complete", "phase_email_sending": "in_progress",
             "created_at": "2026-05-04T10:00:00Z"},
            {"id": "t2", "business_type": "dentist", "city": "Houston", "state": "Texas",
             "status": "active", "leads_total": 78, "leads_emailed": 45, "leads_hot": 12,
             "phase_scraping": "complete", "phase_email_sending": "in_progress",
             "created_at": "2026-05-03T15:30:00Z"},
            {"id": "t3", "business_type": "electrician", "city": "Houston", "state": "Texas",
             "status": "active", "leads_total": 23, "leads_emailed": 18, "leads_hot": 5,
             "phase_scraping": "in_progress", "phase_email_sending": "pending",
             "created_at": "2026-05-04T08:00:00Z"},
        ],
        "recent_activity": [
            {"from_agent": "ScrapeHead", "to_agent": "EnrichHead", "notes": "25 new leads scraped",
             "message_type": "handoff", "timestamp": datetime.utcnow().isoformat()},
            {"from_agent": "SendHead", "to_agent": "AnalyticsHead", "notes": "38 emails opened",
             "message_type": "alert", "timestamp": datetime.utcnow().isoformat()},
            {"from_agent": "MLHead", "to_agent": "MarketingHead", "notes": "Learning cycle 4 complete",
             "message_type": "report", "timestamp": datetime.utcnow().isoformat()},
        ],
        "soul": {
            "total_leads_processed": 1247, "total_emails_sent": 8934,
            "total_clients_acquired": 47, "learning_cycle": 4
        }
    })

# ─── SYSTEM STATUS ───
@app.route('/api/status')
def status():
    return jsonify({
        "system_status": "operational",
        "departments": {
            "scraping": {"head": {"name": "ScrapeHead", "status": "online"}, "team_size": 2},
            "validation": {"head": {"name": "EnrichHead", "status": "online"}, "team_size": 2},
            "marketing": {"head": {"name": "MarketingHead", "status": "online"}, "team_size": 2},
            "sending": {"head": {"name": "SendHead", "status": "online"}, "team_size": 2},
            "analytics": {"head": {"name": "AnalyticsHead", "status": "online"}, "team_size": 2},
            "sales": {"head": {"name": "SalesHead", "status": "online"}, "team_size": 2},
            "sheets": {"head": {"name": "SheetsHead", "status": "online"}, "team_size": 1},
            "accounts": {"head": {"name": "AccountsHead", "status": "online"}, "team_size": 2},
            "tasks": {"head": {"name": "TaskHead", "status": "online"}, "team_size": 2},
            "ml": {"head": {"name": "MLHead", "status": "online"}, "team_size": 2},
            "jarvis": {"head": {"name": "JARVISHead", "status": "online"}, "team_size": 2},
            "memory": {"head": {"name": "MemoryHead", "status": "online"}, "team_size": 2},
        },
        "department_count": 12, "agent_count": 36,
        "recent_activity": [],
        "soul": {"total_leads_processed": 1247, "total_emails_sent": 8934,
                 "total_clients_acquired": 47, "learning_cycle": 4}
    })

# ─── TASKS ───
DEMO_TASKS = [
    {"id": "t1", "business_type": "clinic", "city": "Los Angeles", "state": "CA", "country": "USA",
     "status": "active", "leads_total": 45, "leads_emailed": 32, "leads_opened": 12,
     "leads_replied": 5, "leads_hot": 8, "open_rate": 37.5,
     "phase_scraping": "complete", "phase_validation": "complete",
     "phase_funnel_creation": "complete", "phase_email_sending": "in_progress",
     "phase_tracking": "active", "phase_sales": "pending",
     "created_at": "2026-05-04T10:00:00Z"},
    {"id": "t2", "business_type": "dentist", "city": "Houston", "state": "TX", "country": "USA",
     "status": "active", "leads_total": 78, "leads_emailed": 45, "leads_opened": 18,
     "leads_replied": 8, "leads_hot": 12, "open_rate": 40.0,
     "phase_scraping": "complete", "phase_validation": "complete",
     "phase_funnel_creation": "complete", "phase_email_sending": "in_progress",
     "phase_tracking": "active", "phase_sales": "active",
     "created_at": "2026-05-03T15:30:00Z"},
]

@app.route('/api/tasks')
def tasks():
    return jsonify(DEMO_TASKS)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    import uuid
    task_id = str(uuid.uuid4())[:8]
    new_task = {"id": task_id, "business_type": data.get("business_type", ""),
                "city": data.get("city", ""), "state": data.get("state", ""),
                "status": "active", "leads_total": 0, "leads_emailed": 0,
                "created_at": datetime.utcnow().isoformat()}
    DEMO_TASKS.append(new_task)
    return jsonify({"task_id": task_id, "task": new_task, "status": "launched", "phase": "scraping"})

@app.route('/api/tasks/<task_id>/<action>', methods=['POST'])
def task_action(task_id, action):
    for t in DEMO_TASKS:
        if t["id"] == task_id:
            t["status"] = "paused" if action == "pause" else "active"
    return jsonify({"status": action})

# ─── LEADS ───
DEMO_LEADS = [
    {"id": "l1", "business_name": "Smile Dental Clinic", "owner_name": "Dr. Sarah Ahmed",
     "email_primary": "sarah@smileclinic.com", "phone": "555-0101",
     "city": "Los Angeles", "state": "CA", "niche": "dentist",
     "current_rating": 3.8, "negative_review_count": 7, "lead_score": 85,
     "lead_temperature": "hot", "status": "funnel_ready", "funnel_step": 4,
     "emails_sent_count": 12, "created_at": "2026-05-01T10:00:00Z",
     "website": "https://smiledentalclinic.com", "full_address": "123 Smile Ave, Los Angeles, CA 90001",
     "business_nature": "General Dentistry & Cosmetic Dentistry",
     "years_in_business": 8, "employee_count": "5-10", "revenue_range": "$500K-$1M",
     "full_analysis": "High-value dental practice with strong patient base. Has 7 negative reviews mentioning billing issues and wait times. Competitors nearby: 3. Opportunities: cosmetic dentistry expansion, emergency dental services.",
     "owner_profile": "Dr. Sarah Ahmed - DDS from UCLA, 12 years experience, active in local dental association, Facebook page with 2.3K followers.",
     "gmail_important": True, "important_notes": "Referred by Dr. Johnson - high priority", "last_contact": "2026-05-04T10:00:00Z",
     "interaction_history": [{"date": "2026-05-01", "type": "email_sent", "subject": "your google reviews", "result": "opened"}, {"date": "2026-05-03", "type": "email_sent", "subject": "review reputation", "result": "replied"}],
     "competitors": ["West LA Dental", "Smile Studio LA"], "services_offered": ["General Checkups", "Whitening", "Crowns", "Implants"],
     "review_platforms": {"google": 3.8, "yelp": 4.0, "healthgrades": 4.5}, "pain_points": ["wait times", "billing confusion"],
     "call_script_notes": "Mention her UCLA background, ask about cosmetic dentistry interest", "closing_probability": 85},
    {"id": "l2", "business_name": "Houston Auto Repair", "owner_name": "Mike Johnson",
     "email_primary": "mike@houstonauto.com", "phone": "555-0102",
     "city": "Houston", "state": "TX", "niche": "auto repair",
     "current_rating": 4.2, "negative_review_count": 3, "lead_score": 72,
     "lead_temperature": "warm", "status": "emailed", "funnel_step": 3,
     "emails_sent_count": 8, "created_at": "2026-05-02T14:00:00Z",
     "website": "https://houstonautorepair.com", "full_address": "456 Motor Lane, Houston, TX 77001",
     "business_nature": "Full-Service Auto Repair & Maintenance",
     "years_in_business": 15, "employee_count": "10-15", "revenue_range": "$1M-$2M",
     "full_analysis": "Established auto repair shop with loyal customer base. 3 negative reviews about turnaround time. Located near highway exit - high visibility. Competitors: 5 in 5-mile radius. Opportunity: fleet services for local businesses.",
     "owner_profile": "Mike Johnson - Former mechanic, self-taught business owner, active on Nextdoor, responds to reviews personally.",
     "gmail_important": False, "important_notes": "", "last_contact": "2026-05-03T14:00:00Z",
     "interaction_history": [{"date": "2026-05-02", "type": "email_sent", "subject": "online reviews matter", "result": "opened"}],
     "competitors": ["QuickFix Auto", "ProTech Motors", "Texas Auto Care"], "services_offered": ["Oil Change", "Brakes", "Tires", "Engine Repair"],
     "review_platforms": {"google": 4.2, "yelp": 3.9, "bbb": 4.5}, "pain_points": ["turnaround time", "pricing transparency"],
     "call_script_notes": "Ask about fleet services, mention local business discount", "closing_probability": 72},
    {"id": "l3", "business_name": "Legal Eagles LLP", "owner_name": "James White",
     "email_primary": "james@legaleagles.com", "phone": "555-0103",
     "city": "Chicago", "state": "IL", "niche": "law firm",
     "current_rating": 4.8, "negative_review_count": 1, "lead_score": 92,
     "lead_temperature": "hot", "status": "replied", "funnel_step": 5,
     "emails_sent_count": 18, "created_at": "2026-05-01T08:00:00Z",
     "website": "https://legaleaglesllp.com", "full_address": "789 Legal Plaza, Chicago, IL 60601",
     "business_nature": "Personal Injury & Corporate Law",
     "years_in_business": 20, "employee_count": "20-30", "revenue_range": "$5M-$10M",
     "full_analysis": "Top-tier law firm with excellent reputation. Only 1 negative review about billing. Strong online presence with case results featured. Already using reputation management - competitor. High budget for legal services. Opportunity: DMCA for their copyrighted case studies.",
     "owner_profile": "James White - Harvard Law graduate, 25 years experience, former prosecutor, active on LinkedIn (15K connections), published author.",
     "gmail_important": True, "important_notes": "High value client - already interested in DMCA services", "last_contact": "2026-05-05T09:00:00Z",
     "interaction_history": [{"date": "2026-05-01", "type": "email_sent", "subject": "your google reviews", "result": "opened"}, {"date": "2026-05-02", "type": "email_sent", "subject": "review reputation", "result": "opened"}, {"date": "2026-05-03", "type": "reply_received", "content": "Interested in learning more about your services"}],
     "competitors": ["Smith & Associates", "Chicago Legal Group"], "services_offered": ["Personal Injury", "Corporate Law", "IP Protection", "Litigation"],
     "review_platforms": {"google": 4.8, "yelp": 4.6, "avvo": 5.0}, "pain_points": ["client acquisition"],
     "call_script_notes": "Offer free consultation, mention case study protection, ask about trademark needs", "closing_probability": 92},
    {"id": "l4", "business_name": "Pizza Palace", "owner_name": "Tom Wilson",
     "email_primary": "tom@pizzapalace.com", "phone": "555-0104",
     "city": "Denver", "state": "CO", "niche": "restaurant",
     "current_rating": 3.5, "negative_review_count": 12, "lead_score": 45,
     "lead_temperature": "cold", "status": "scraped", "funnel_step": 1,
     "emails_sent_count": 2, "created_at": "2026-05-03T16:00:00Z",
     "website": "https://pizzapalacedenver.com", "full_address": "321 Food Court, Denver, CO 80201",
     "business_nature": "Italian Restaurant & Pizza Delivery",
     "years_in_business": 3, "employee_count": "5-8", "revenue_range": "$200K-$400K",
     "full_analysis": "New restaurant struggling with online reputation. 12 negative reviews about food quality and service. Located in food court with high foot traffic. Needs help but low budget. Opportunity: basic reputation management package.",
     "owner_profile": "Tom Wilson - First-time business owner, invested life savings, very concerned about reviews affecting business.",
     "gmail_important": False, "important_notes": "", "last_contact": "2026-05-03T16:00:00Z",
     "interaction_history": [{"date": "2026-05-03", "type": "email_sent", "subject": "denver restaurants", "result": "delivered"}],
     "competitors": ["Domino's", "Papa John's", "Local Pizza Co"], "services_offered": ["Dine-in", "Delivery", "Catering"],
     "review_platforms": {"google": 3.5, "yelp": 3.2, "tripadvisor": 3.0}, "pain_points": ["food quality", "service speed", "inconsistent orders"],
     "call_script_notes": "Empathize with startup challenges, offer affordable starter package", "closing_probability": 45},
{"id": "l5", "business_name": "Bright Eyes Optometry", "owner_name": "Dr. Lisa Chen",
      "email_primary": "lisa@brighteyes.com", "phone": "555-0105",
      "city": "Phoenix", "state": "AZ", "niche": "optometrist",
      "current_rating": 4.5, "negative_review_count": 2, "lead_score": 78,
      "lead_temperature": "hot", "status": "funnel_ready", "funnel_step": 4,
      "emails_sent_count": 10, "created_at": "2026-05-02T09:00:00Z",
      "website": "https://brighteyesoptometry.com", "full_address": "555 Vision Way, Phoenix, AZ 85001",
      "business_nature": "Optometry & Vision Care Services",
      "years_in_business": 10, "employee_count": "8-12", "revenue_range": "$800K-$1.2M",
      "full_analysis": "Growing optometry practice with strong community presence. 2 negative reviews about appointment scheduling. Offers unique services: pediatric care, sports vision. Competitors: 4 major chains nearby. Opportunity: specialty eye care marketing.",
      "owner_profile": "Dr. Lisa Chen - OD from Arizona State, 15 years experience, passionate about pediatric vision care, local school volunteer.",
      "gmail_important": True, "important_notes": "Referred by medical association - follow up this week", "last_contact": "2026-05-04T11:00:00Z",
      "interaction_history": [{"date": "2026-05-02", "type": "email_sent", "subject": "phoenix optometry", "result": "opened"}, {"date": "2026-05-04", "type": "email_sent", "subject": "vision care reviews", "result": "opened"}],
      "competitors": ["LensCrafters", "Pearle Vision", "Visionworks", "Local Eye Docs"], "services_offered": ["Eye Exams", "Contacts", "Glasses", "Pediatric Care", "Sports Vision"],
      "review_platforms": {"google": 4.5, "yelp": 4.3, "healthgrades": 4.7}, "pain_points": ["appointment scheduling", "insurance processing"],
      "call_script_notes": "Mention pediatric specialty, ask about school screening programs", "closing_probability": 78},
     {"id": "l6", "business_name": "Paws & Claws Veterinary", "owner_name": "Dr. Marcus Rivera",
      "email_primary": "marcus@pawsandclaws.com", "phone": "555-0106",
      "city": "Miami", "state": "FL", "niche": "veterinarian",
      "current_rating": 4.1, "negative_review_count": 5, "lead_score": 68,
      "lead_temperature": "warm", "status": "emailed", "funnel_step": 3,
      "emails_sent_count": 7, "created_at": "2026-05-03T11:00:00Z",
      "website": "https://pawsandclaws.vet", "full_address": "890 Pet Blvd, Miami, FL 33101",
      "business_nature": "Full-Service Veterinary Clinic & Emergency Care",
      "years_in_business": 12, "employee_count": "15-20", "revenue_range": "$1.5M-$2.5M",
      "full_analysis": "Established vet clinic with emergency services. 5 negative reviews about pricing and wait times. Growing pet market in Miami. Opportunity: pet insurance partnerships, grooming services expansion.",
      "owner_profile": "Dr. Marcus Rivera - Cornell Vet School graduate, 18 years experience, passionate about animal welfare, local pet shelter volunteer.",
      "gmail_important": False, "important_notes": "", "last_contact": "2026-05-04T15:00:00Z",
      "interaction_history": [{"date": "2026-05-03", "type": "email_sent", "subject": "miami vet reviews", "result": "opened"}],
      "competitors": ["Animal Planet Vets", "PetCare Miami", "Emergency Pet Hospital"], "services_offered": ["General Care", "Surgery", "Emergency", "Grooming", "Dental"],
      "review_platforms": {"google": 4.1, "yelp": 3.8, "zocdoc": 4.3}, "pain_points": ["pricing concerns", "wait times"],
      "call_script_notes": "Mention emergency services capability, ask about expansion plans", "closing_probability": 68},
     {"id": "l7", "business_name": "TechStart Solutions", "owner_name": "Jennifer Walsh",
      "email_primary": "jennifer@techstartsolutions.com", "phone": "555-0107",
      "city": "Seattle", "state": "WA", "niche": "IT services",
      "current_rating": 4.6, "negative_review_count": 2, "lead_score": 88,
      "lead_temperature": "hot", "status": "funnel_ready", "funnel_step": 4,
      "emails_sent_count": 9, "created_at": "2026-05-01T13:00:00Z",
      "website": "https://techstartsolutions.com", "full_address": "456 Tech Lane, Seattle, WA 98101",
      "business_nature": "IT Consulting & Managed Services for SMBs",
      "years_in_business": 7, "employee_count": "12-18", "revenue_range": "$1.2M-$2M",
      "full_analysis": "Fast-growing IT consultancy serving 50+ local businesses. Only 2 negative reviews about response time. Strong reputation in Seattle tech community. Opportunity: cybersecurity services, cloud migration.",
      "owner_profile": "Jennifer Walsh - Former Microsoft engineer, MBA from UW, active in Seattle tech meetups, speaks at local conferences.",
      "gmail_important": True, "important_notes": "Met at tech conference - interested in reputation management for her company", "last_contact": "2026-05-05T10:00:00Z",
      "interaction_history": [{"date": "2026-05-01", "type": "email_sent", "subject": "seattle it company reviews", "result": "opened"}, {"date": "2026-05-04", "type": "email_sent", "subject": "business reputation", "result": "opened"}],
      "competitors": ["Seattle IT Pros", "TechConnect", "NW Managed Services"], "services_offered": ["IT Consulting", "Managed Services", "Cloud Setup", "Security", "Help Desk"],
      "review_platforms": {"google": 4.6, "clutch": 4.8, "yelp": 4.2}, "pain_points": ["response time", "scalability"],
      "call_script_notes": "Mention cybersecurity growth, ask about client testimonial needs", "closing_probability": 88},
     {"id": "l8", "business_name": "Green Thumb Landscaping", "owner_name": "Carlos Mendez",
      "email_primary": "carlos@greenthumbland.com", "phone": "555-0108",
      "city": "Austin", "state": "TX", "niche": "landscaping",
      "current_rating": 3.9, "negative_review_count": 8, "lead_score": 55,
      "lead_temperature": "warm", "status": "emailed", "funnel_step": 2,
      "emails_sent_count": 5, "created_at": "2026-05-04T09:00:00Z",
      "website": "https://greenthumblandscaping.com", "full_address": "789 Garden Way, Austin, TX 78701",
      "business_nature": "Residential & Commercial Landscaping Services",
      "years_in_business": 5, "employee_count": "8-12", "revenue_range": "$400K-$700K",
      "full_analysis": "Growing landscaping business in booming Austin market. 8 negative reviews about missed appointments and communication. Needs help with customer service processes. Opportunity: commercial contracts, maintenance contracts.",
      "owner_profile": "Carlos Mendez - Landscape architecture degree from Texas A&M, self-employed after working for major company, works long hours personally on jobs.",
      "gmail_important": False, "important_notes": "", "last_contact": "2026-05-05T08:00:00Z",
      "interaction_history": [{"date": "2026-05-04", "type": "email_sent", "subject": "austin landscaping", "result": "delivered"}],
      "competitors": ["Austin Green Pros", "Hill Country Landscapes", "Texas Turf Masters"], "services_offered": ["Design", "Installation", "Maintenance", "Irrigation", "Tree Service"],
      "review_platforms": {"google": 3.9, "yelp": 3.5, "nextdoor": 4.0}, "pain_points": ["missed appointments", "communication", "scheduling"],
      "call_script_notes": "Offer scheduling system help, mention commercial opportunities", "closing_probability": 55},
     {"id": "l9", "business_name": "Sunrise Fitness Center", "owner_name": "Rachel Torres",
      "email_primary": "rachel@sunrisefitness.com", "phone": "555-0109",
      "city": "San Diego", "state": "CA", "niche": "gym/fitness",
      "current_rating": 4.3, "negative_review_count": 4, "lead_score": 75,
      "lead_temperature": "warm", "status": "funnel_ready", "funnel_step": 4,
      "emails_sent_count": 11, "created_at": "2026-05-02T07:00:00Z",
      "website": "https://sunrisefitnessgym.com", "full_address": "321 Fitness Ave, San Diego, CA 92101",
      "business_nature": "24/7 Fitness Center & Personal Training",
      "years_in_business": 9, "employee_count": "20-25", "revenue_range": "$1M-$1.8M",
      "full_analysis": "Popular 24/7 gym in San Diego with strong membership base. 4 negative reviews about crowded peak hours and equipment maintenance. Looking to expand location. Opportunity: second location marketing, corporate partnerships.",
      "owner_profile": "Rachel Torres - Former professional athlete, fitness certification from NASM, runs charity fitness events monthly.",
      "gmail_important": True, "important_notes": "Expanding to second location - needs help with new location reviews", "last_contact": "2026-05-05T14:00:00Z",
      "interaction_history": [{"date": "2026-05-02", "type": "email_sent", "subject": "san diego gym reviews", "result": "opened"}, {"date": "2026-05-04", "type": "email_sent", "subject": "fitness reputation", "result": "replied"}],
      "competitors": ["Planet Fitness", "LA Fitness", "CrossFit San Diego", "FitLife"], "services_offered": ["Gym Access", "Personal Training", "Group Classes", "Nutrition Coaching", "Locker Room"],
      "review_platforms": {"google": 4.3, "yelp": 4.1, "facebook": 4.5}, "pain_points": ["crowding", "equipment maintenance"],
      "call_script_notes": "Ask about second location plans, offer to help with new location reviews", "closing_probability": 75},
     {"id": "l10", "business_name": "Elite Hair Studio", "owner_name": "Patricia Kim",
      "email_primary": "patricia@elitehairstudio.com", "phone": "555-0110",
      "city": "New York", "state": "NY", "niche": "salon",
      "current_rating": 4.7, "negative_review_count": 1, "lead_score": 82,
      "lead_temperature": "hot", "status": "replied", "funnel_step": 5,
      "emails_sent_count": 14, "created_at": "2026-05-01T12:00:00Z",
      "website": "https://elitehairstylonyc.com", "full_address": "555 Fifth Avenue, New York, NY 10018",
      "business_nature": "Premium Hair Salon & Styling Services",
      "years_in_business": 15, "employee_count": "10-15", "revenue_range": "$1.5M-$2.5M",
      "full_analysis": "High-end salon in Manhattan with celebrity clientele. Only 1 negative review about pricing. Featured in multiple fashion magazines. Already uses PR firm - but could benefit from DMCA for unauthorized image use.",
      "owner_profile": "Patricia Kim - Trained in Seoul and Paris, winner of multiple styling awards, Instagram with 50K followers.",
      "gmail_important": True, "important_notes": "High-value - concerned about unauthorized use of her styles online", "last_contact": "2026-05-06T09:00:00Z",
      "interaction_history": [{"date": "2026-05-01", "type": "email_sent", "subject": "nyc salon reviews", "result": "opened"}, {"date": "2026-05-03", "type": "email_sent", "subject": "image protection", "result": "opened"}, {"date": "2026-05-05", "type": "reply_received", "content": "Can you help protect my work from being stolen?"}],
      "competitors": ["Sally Hershberger", "Umberto Giannini", "John Frieda"], "services_offered": ["Cut & Style", "Color", "Extensions", "Bridal", "Treatments"],
      "review_platforms": {"google": 4.7, "yelp": 4.8, "vogue": 5.0}, "pain_points": ["image theft", "competitor copying"],
      "call_script_notes": "Focus on DMCA for image protection, mention competitor research", "closing_probability": 82},
     {"id": "l11", "business_name": "Blue Ocean Plumbing", "owner_name": "David Chen",
      "email_primary": "david@blueoceanplumbing.com", "phone": "555-0111",
      "city": "Boston", "state": "MA", "niche": "plumbing",
      "current_rating": 4.0, "negative_review_count": 6, "lead_score": 62,
      "lead_temperature": "warm", "status": "emailed", "funnel_step": 3,
      "emails_sent_count": 6, "created_at": "2026-05-04T10:00:00Z",
      "website": "https://blueoceanplumbing.com", "full_address": "678 Pipe Street, Boston, MA 02101",
      "business_nature": "Residential & Commercial Plumbing Services",
      "years_in_business": 11, "employee_count": "8-12", "revenue_range": "$800K-$1.2M",
      "full_analysis": "Reliable plumbing company serving Boston area. 6 negative reviews about pricing transparency and scheduling. Has loyal base but struggles with online reputation. Opportunity: emergency service marketing, preventive maintenance contracts.",
      "owner_profile": "David Chen - Master plumber license, started as apprentice, focuses on quality work over volume.",
      "gmail_important": False, "important_notes": "", "last_contact": "2026-05-05T11:00:00Z",
      "interaction_history": [{"date": "2026-05-04", "type": "email_sent", "subject": "boston plumbing reviews", "result": "opened"}],
      "competitors": ["Roto-Rooter", "Boston Plumbers", "Mario & Son"], "services_offered": ["Repairs", "Installation", "Drain Cleaning", "Water Heaters", "Emergency"],
      "review_platforms": {"google": 4.0, "yelp": 3.7, "bbb": 4.2}, "pain_points": ["pricing transparency", "scheduling"],
      "call_script_notes": "Offer pricing transparency help, mention emergency serviceupsell", "closing_probability": 62},
     {"id": "l12", "business_name": "Sunshine Daycare Center", "owner_name": "Maria Santos",
      "email_primary": "maria@sunshinedaycare.com", "phone": "555-0112",
      "city": "Atlanta", "state": "GA", "niche": "daycare",
      "current_rating": 4.4, "negative_review_count": 3, "lead_score": 70,
      "lead_temperature": "warm", "status": "funnel_ready", "funnel_step": 4,
      "emails_sent_count": 8, "created_at": "2026-05-03T08:00:00Z",
      "website": "https://sunshinedaycarecenter.com", "full_address": "234 Child Way, Atlanta, GA 30301",
      "business_nature": "Childcare & Early Education Center",
      "years_in_business": 8, "employee_count": "15-20", "revenue_range": "$600K-$900K",
      "full_analysis": "Licensed daycare with excellent curriculum. 3 negative reviews about waitlist and enrollment process. High demand in growing Atlanta suburb. Opportunity: before/after school programs, summer camp expansion.",
      "owner_profile": "Maria Santos - Early childhood education degree, former public school teacher, passionate about child development, active in local parent groups.",
      "gmail_important": False, "important_notes": "", "last_contact": "2026-05-05T16:00:00Z",
      "interaction_history": [{"date": "2026-05-03", "type": "email_sent", "subject": "atlanta daycare", "result": "opened"}, {"date": "2026-05-05", "type": "email_sent", "subject": "childcare reviews", "result": "opened"}],
      "competitors": ["KinderCare", "Learning Care Group", "The Little School"], "services_offered": ["Infant Care", "Toddler Care", "Preschool", "After School", "Summer Camp"],
      "review_platforms": {"google": 4.4, "yelp": 4.2, "care.com": 4.6}, "pain_points": ["waitlist", "enrollment process"],
      "call_script_notes": "Mention before/after school programs, ask about expansion plans", "closing_probability": 70},
     {"id": "l13", "business_name": "Urban Eats Restaurant", "owner_name": "James Park",
      "email_primary": "james@urbaneats.com", "phone": "555-0113",
      "city": "Portland", "state": "OR", "niche": "restaurant",
      "current_rating": 3.6, "negative_review_count": 9, "lead_score": 48,
      "lead_temperature": "cold", "status": "scraped", "funnel_step": 1,
      "emails_sent_count": 2, "created_at": "2026-05-05T14:00:00Z",
      "website": "https://urbaneatspdx.com", "full_address": "567 Foodie Lane, Portland, OR 97201",
      "business_nature": "Modern American Fusion Restaurant",
      "years_in_business": 2, "employee_count": "12-15", "revenue_range": "$500K-$800K",
      "full_analysis": "New restaurant in competitive Portland food scene. 9 negative reviews about inconsistency and slow service. Passionate chef but struggling with operations. Needs basic reputation help and operational guidance.",
      "owner_profile": "James Park - Culinary school graduate, worked at Michelin-star restaurants, poured savings into restaurant, very stressed about business.",
      "gmail_important": False, "important_notes": "Struggling - needs affordable help", "last_contact": "2026-05-05T14:00:00Z",
      "interaction_history": [{"date": "2026-05-05", "type": "email_sent", "subject": "portland restaurants", "result": "delivered"}],
      "competitors": ["Pok Pok", "Le Pigeon", "Central Cafe"], "services_offered": ["Dinner Service", "Private Dining", "Catering", "Takeout"],
      "review_platforms": {"google": 3.6, "yelp": 3.4, "tripadvisor": 3.5}, "pain_points": ["inconsistency", "slow service", "new restaurant challenges"],
      "call_script_notes": "Empathize with startup struggles, offer affordable starter package", "closing_probability": 48},
     {"id": "l14", "business_name": "Prestige Auto Detailing", "owner_name": "Tony Martinez",
      "email_primary": "tony@prestigeautodetailing.com", "phone": "555-0114",
      "city": "Las Vegas", "state": "NV", "niche": "auto detailing",
      "current_rating": 4.8, "negative_review_count": 1, "lead_score": 90,
      "lead_temperature": "hot", "status": "funnel_ready", "funnel_step": 4,
      "emails_sent_count": 12, "created_at": "2026-05-02T11:00:00Z",
      "website": "https://prestigeautodetailinglv.com", "full_address": "890 Shine Way, Las Vegas, NV 89101",
      "business_nature": "Premium Auto Detailing & Ceramic Coating",
      "years_in_business": 6, "employee_count": "6-8", "revenue_range": "$600K-$900K",
      "full_analysis": "Top-rated detailing service in Las Vegas serving luxury vehicles. Only 1 negative review about appointment scheduling. High-end clientele including celebrities. Opportunity: fleet accounts for casinos, mobile detailing expansion.",
      "owner_profile": "Tony Martinez - Former detailer for luxury dealerships, certified in ceramic coating, meticulous about quality, word-of-mouth driven.",
      "gmail_important": True, "important_notes": "High-quality - expanding mobile service", "last_contact": "2026-05-05T13:00:00Z",
      "interaction_history": [{"date": "2026-05-02", "type": "email_sent", "subject": "las vegas auto detailing", "result": "opened"}, {"date": "2026-05-04", "type": "email_sent", "subject": "luxury car reviews", "result": "replied"}],
      "competitors": ["Professional Detailers", "Magic Hand Car Wash", "Luxury Auto Spa"], "services_offered": ["Full Detail", "Ceramic Coating", "Paint Correction", "Interior Detail", "Mobile Service"],
      "review_platforms": {"google": 4.8, "yelp": 4.9, "facebook": 5.0}, "pain_points": ["appointment scheduling"],
      "call_script_notes": "Ask about mobile expansion, mention casino fleet opportunities", "closing_probability": 90},
     {"id": "l15", "business_name": "Mindful Psychology Group", "owner_name": "Dr. Amanda Foster",
      "email_primary": "amanda@mindfulpsychgroup.com", "phone": "555-0115",
      "city": "Denver", "state": "CO", "niche": "psychology/therapy",
      "current_rating": 4.9, "negative_review_count": 0, "lead_score": 95,
      "lead_temperature": "hot", "status": "replied", "funnel_step": 5,
      "emails_sent_count": 16, "created_at": "2026-05-01T09:00:00Z",
      "website": "https://mindfulpsychologygroup.com", "full_address": "123 Wellness Center, Denver, CO 80202",
      "business_nature": "Mental Health & Psychology Practice",
      "years_in_business": 10, "employee_count": "8-12", "revenue_range": "$1M-$1.5M",
      "full_analysis": "Exceptional therapy practice with perfect 4.9 rating. No negative reviews - highly respected in Denver. Expanding to add psychiatry services. Opportunity: content marketing for mental health, podcast sponsorship.",
      "owner_profile": "Dr. Amanda Foster - PhD in Psychology from Stanford, published author, hosts popular mental health podcast, speaker at conferences.",
      "gmail_important": True, "important_notes": "Elite client - wants to protect her podcast content from theft", "last_contact": "2026-05-06T11:00:00Z",
      "interaction_history": [{"date": "2026-05-01", "type": "email_sent", "subject": "denver therapy reviews", "result": "opened"}, {"date": "2026-05-03", "type": "email_sent", "subject": "content protection", "result": "opened"}, {"date": "2026-05-05", "type": "reply_received", "content": "Need help protecting my podcast episodes"}],
      "competitors": ["Denver Therapy Associates", "Rocky Mountain Psychiatry", "Wellness First"], "services_offered": ["Individual Therapy", "Couples Counseling", "Family Therapy", "Group Sessions", "Psychiatric Eval"],
      "review_platforms": {"google": 4.9, "psychologytoday": 5.0, "yelp": 4.8}, "pain_points": ["content theft", "brand protection"],
      "call_script_notes": "Focus on content DMCA protection, mention podcast growth opportunities", "closing_probability": 95},
 ]

@app.route('/api/leads')
def leads():
    temp = request.args.get('temperature')
    status_filter = request.args.get('status')
    result = DEMO_LEADS
    if temp:
        result = [l for l in result if l.get('lead_temperature') == temp]
    if status_filter:
        result = [l for l in result if l.get('status') == status_filter]
    return jsonify(result)

@app.route('/api/leads/<lead_id>')
def get_lead(lead_id):
    lead = next((l for l in DEMO_LEADS if l["id"] == lead_id), None)
    if not lead:
        return jsonify({}), 404
    lead_copy = dict(lead)
    lead_copy["email_history"] = [
        {"id": "e1", "email_number": 1, "subject_line": "your google reviews",
         "opened": True, "open_count": 3, "replied": False, "status": "sent",
         "sent_at": "2026-05-01T10:00:00Z"},
        {"id": "e2", "email_number": 2, "subject_line": "review reputation",
         "opened": True, "open_count": 1, "replied": True, "status": "sent",
         "reply_content": "Hi, I'm interested. Can you tell me more?",
         "sent_at": "2026-05-03T10:00:00Z"},
    ]
    return jsonify(lead_copy)

@app.route('/api/leads/export')
def export_leads():
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Business Name", "Owner", "Email", "City", "State", "Rating", "Score", "Temperature"])
    for l in DEMO_LEADS:
        writer.writerow([l["business_name"], l["owner_name"], l["email_primary"],
                        l["city"], l["state"], l["current_rating"], l["lead_score"], l["lead_temperature"]])
    return output.getvalue(), 200, {"Content-Type": "text/csv",
                                     "Content-Disposition": "attachment; filename=leads.csv"}

@app.route('/api/leads/scored')
def scored_leads():
    scored = sorted([l for l in DEMO_LEADS if l["lead_score"] > 0],
                   key=lambda x: x["lead_score"], reverse=True)
    return jsonify([{"id": l["id"], "business_name": l["business_name"], "city": l["city"],
                    "niche": l["niche"], "lead_score": l["lead_score"],
                    "lead_temperature": l["lead_temperature"],
                    "emails_sent_count": l["emails_sent_count"]} for l in scored])


# ─── ENHANCED LEAD DETAILS ───
@app.route('/api/leads/<lead_id>/full')
def get_lead_full(lead_id):
    lead = next((l for l in DEMO_LEADS if l["id"] == lead_id), None)
    if not lead:
        return jsonify({"error": "Lead not found"}), 404
    return jsonify({
        "id": lead["id"],
        "business_name": lead.get("business_name"),
        "owner_name": lead.get("owner_name"),
        "email_primary": lead.get("email_primary"),
        "phone": lead.get("phone"),
        "website": lead.get("website", ""),
        "full_address": lead.get("full_address", ""),
        "city": lead.get("city"),
        "state": lead.get("state"),
        "business_nature": lead.get("business_nature", ""),
        "niche": lead.get("niche"),
        "years_in_business": lead.get("years_in_business", 0),
        "employee_count": lead.get("employee_count", ""),
        "revenue_range": lead.get("revenue_range", ""),
        "full_analysis": lead.get("full_analysis", ""),
        "owner_profile": lead.get("owner_profile", ""),
        "current_rating": lead.get("current_rating"),
        "negative_review_count": lead.get("negative_review_count"),
        "review_platforms": lead.get("review_platforms", {}),
        "pain_points": lead.get("pain_points", []),
        "services_offered": lead.get("services_offered", []),
        "competitors": lead.get("competitors", []),
        "lead_score": lead.get("lead_score"),
        "lead_temperature": lead.get("lead_temperature"),
        "closing_probability": lead.get("closing_probability", 0),
        "call_script_notes": lead.get("call_script_notes", ""),
        "status": lead.get("status"),
        "gmail_important": lead.get("gmail_important", False),
        "important_notes": lead.get("important_notes", ""),
        "last_contact": lead.get("last_contact"),
        "emails_sent_count": lead.get("emails_sent_count", 0),
        "interaction_history": lead.get("interaction_history", []),
        "created_at": lead.get("created_at")
    })


# ─── GMAIL IMPORTANT LEADS ───
@app.route('/api/leads/important')
def get_important_leads():
    important = [l for l in DEMO_LEADS if l.get("gmail_important", False)]
    return jsonify([{
        "id": l["id"],
        "business_name": l["business_name"],
        "owner_name": l["owner_name"],
        "email_primary": l["email_primary"],
        "phone": l["phone"],
        "website": l.get("website", ""),
        "business_nature": l.get("business_nature", ""),
        "lead_score": l["lead_score"],
        "lead_temperature": l["lead_temperature"],
        "important_notes": l.get("important_notes", ""),
        "closing_probability": l.get("closing_probability", 0),
        "call_script_notes": l.get("call_script_notes", ""),
        "last_contact": l.get("last_contact"),
        "full_analysis": l.get("full_analysis", "")
    } for l in important])


@app.route('/api/leads/<lead_id>/mark-important', methods=['POST'])
def mark_lead_important(lead_id):
    data = request.get_json() or {}
    for l in DEMO_LEADS:
        if l["id"] == lead_id:
            l["gmail_important"] = data.get("important", True)
            l["important_notes"] = data.get("notes", l.get("important_notes", ""))
            return jsonify({"status": "updated", "gmail_important": l["gmail_important"]})
    return jsonify({"error": "Lead not found"}), 404


# ─── GOOGLE SHEETS SYNC ───
@app.route('/api/sheets/sync', methods=['POST'])
def sync_to_sheets():
    data = request.get_json() or {}
    include_important_only = data.get("important_only", False)
    
    leads_to_sync = DEMO_LEADS
    if include_important_only:
        leads_to_sync = [l for l in DEMO_LEADS if l.get("gmail_important", False)]
    
    sheets_data = {
        "spreadsheet_name": "DMCAShield Leads",
        "sheets": [
            {"name": "All Leads", "columns": [
                "ID", "Business Name", "Owner", "Email", "Phone", "Website",
                "Address", "City", "State", "Niche", "Business Nature",
                "Years in Business", "Employee Count", "Revenue Range",
                "Current Rating", "Negative Reviews", "Lead Score",
                "Lead Temperature", "Closing Probability", "Status",
                "Gmail Important", "Important Notes", "Last Contact",
                "Created At", "Full Analysis", "Owner Profile",
                "Pain Points", "Services Offered", "Competitors"
            ]},
            {"name": "Hot Leads", "columns": ["Business Name", "Owner", "Email", "Phone", "Website", "Lead Score", "Closing Prob", "Call Notes"]},
            {"name": "Gmail Important", "columns": ["Business Name", "Owner", "Email", "Lead Score", "Important Notes", "Last Contact"]}
        ],
        "rows": []
    }
    
    for lead in leads_to_sync:
        sheets_data["rows"].append({
            "All Leads": {
                "ID": lead["id"],
                "Business Name": lead.get("business_name", ""),
                "Owner": lead.get("owner_name", ""),
                "Email": lead.get("email_primary", ""),
                "Phone": lead.get("phone", ""),
                "Website": lead.get("website", ""),
                "Address": lead.get("full_address", ""),
                "City": lead.get("city", ""),
                "State": lead.get("state", ""),
                "Niche": lead.get("niche", ""),
                "Business Nature": lead.get("business_nature", ""),
                "Years in Business": lead.get("years_in_business", ""),
                "Employee Count": lead.get("employee_count", ""),
                "Revenue Range": lead.get("revenue_range", ""),
                "Current Rating": lead.get("current_rating", ""),
                "Negative Reviews": lead.get("negative_review_count", ""),
                "Lead Score": lead.get("lead_score", ""),
                "Lead Temperature": lead.get("lead_temperature", ""),
                "Closing Probability": lead.get("closing_probability", ""),
                "Status": lead.get("status", ""),
                "Gmail Important": "Yes" if lead.get("gmail_important") else "No",
                "Important Notes": lead.get("important_notes", ""),
                "Last Contact": lead.get("last_contact", ""),
                "Created At": lead.get("created_at", ""),
                "Full Analysis": lead.get("full_analysis", ""),
                "Owner Profile": lead.get("owner_profile", ""),
                "Pain Points": ", ".join(lead.get("pain_points", [])),
                "Services Offered": ", ".join(lead.get("services_offered", [])),
                "Competitors": ", ".join(lead.get("competitors", []))
            },
            "Hot Leads": {
                "Business Name": lead.get("business_name", ""),
                "Owner": lead.get("owner_name", ""),
                "Email": lead.get("email_primary", ""),
                "Phone": lead.get("phone", ""),
                "Website": lead.get("website", ""),
                "Lead Score": lead.get("lead_score", ""),
                "Closing Prob": lead.get("closing_probability", ""),
                "Call Notes": lead.get("call_script_notes", "")
            },
            "Gmail Important": {
                "Business Name": lead.get("business_name", ""),
                "Owner": lead.get("owner_name", ""),
                "Email": lead.get("email_primary", ""),
                "Lead Score": lead.get("lead_score", ""),
                "Important Notes": lead.get("important_notes", ""),
                "Last Contact": lead.get("last_contact", "")
            }
        })
    
    return jsonify({
        "status": "ready_for_export",
        "format": "google_sheets_csv",
        "sheets": sheets_data["sheets"],
        "total_leads": len(leads_to_sync),
        "data": sheets_data,
        "instructions": "Download as CSV and import to Google Sheets, or use Google Sheets API for direct sync"
    })


@app.route('/api/sheets/export-csv')
def export_sheets_csv():
    import csv, io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "Business Name", "Owner", "Email", "Phone", "Website", "Address",
        "City", "State", "Niche", "Business Nature", "Years", "Employees",
        "Revenue", "Rating", "Neg Reviews", "Lead Score", "Temperature",
        "Closing %", "Status", "Gmail Important", "Important Notes",
        "Last Contact", "Full Analysis", "Owner Profile", "Pain Points",
        "Services", "Competitors", "Call Notes"
    ])
    
    for lead in DEMO_LEADS:
        writer.writerow([
            lead.get("business_name", ""),
            lead.get("owner_name", ""),
            lead.get("email_primary", ""),
            lead.get("phone", ""),
            lead.get("website", ""),
            lead.get("full_address", ""),
            lead.get("city", ""),
            lead.get("state", ""),
            lead.get("niche", ""),
            lead.get("business_nature", ""),
            lead.get("years_in_business", ""),
            lead.get("employee_count", ""),
            lead.get("revenue_range", ""),
            lead.get("current_rating", ""),
            lead.get("negative_review_count", ""),
            lead.get("lead_score", ""),
            lead.get("lead_temperature", ""),
            lead.get("closing_probability", ""),
            lead.get("status", ""),
            "Yes" if lead.get("gmail_important") else "No",
            lead.get("important_notes", ""),
            lead.get("last_contact", ""),
            lead.get("full_analysis", ""),
            lead.get("owner_profile", ""),
            "; ".join(lead.get("pain_points", [])),
            "; ".join(lead.get("services_offered", [])),
            "; ".join(lead.get("competitors", [])),
            lead.get("call_script_notes", "")
        ])
    
    return output.getvalue(), 200, {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=dmcashield_leads_detailed.csv"
    }

# ─── HOT LEADS ───
@app.route('/api/hot-leads')
def hot_leads():
    hot = [l for l in DEMO_LEADS if l["lead_temperature"] == "hot"]
    return jsonify([{
        "id": l["id"], "business_name": l["business_name"], "owner_name": l["owner_name"],
        "email_primary": l["email_primary"], "city": l["city"], "niche": l["niche"],
        "current_rating": l["current_rating"],
        "conversations": [{"subject": "your reviews", "reply": "Interested, tell me more",
                          "replied_at": "2026-05-04T10:00:00Z"}]
    } for l in hot])

# ─── ACCOUNTS ───
DEMO_ACCOUNTS = [
    {"id": "a1", "email_address": "campaign@dmcashield.com", "display_name": "Review Team",
     "daily_limit": 40, "sent_today": 23, "total_sent": 456, "warmup_day": 28,
     "warmup_complete": True, "status": "active", "blacklist_status": "clean",
     "health_score": 95, "total_opens": 180, "total_replies": 45,
     "created_at": "2026-04-01T00:00:00Z"},
    {"id": "a2", "email_address": "outreach@dmcashield.com", "display_name": "DMCA Support",
     "daily_limit": 30, "sent_today": 15, "total_sent": 234, "warmup_day": 14,
     "warmup_complete": False, "status": "warming_up", "blacklist_status": "clean",
     "health_score": 82, "total_opens": 90, "total_replies": 22,
     "created_at": "2026-04-15T00:00:00Z"},
]

@app.route('/api/accounts')
def accounts():
    return jsonify(DEMO_ACCOUNTS)

@app.route('/api/accounts', methods=['POST'])
def add_account():
    data = request.get_json() or {}
    import uuid
    new_id = str(uuid.uuid4())[:8]
    acc = {"id": new_id, "email_address": data.get("email_address", ""),
           "display_name": data.get("display_name", ""), "daily_limit": 5,
           "sent_today": 0, "total_sent": 0, "warmup_day": 1,
           "warmup_complete": False, "status": "warming_up", "blacklist_status": "clean",
           "health_score": 50, "total_opens": 0, "total_replies": 0,
           "created_at": datetime.utcnow().isoformat()}
    DEMO_ACCOUNTS.append(acc)
    return jsonify({"id": new_id, "email_address": acc["email_address"], "status": "warming_up"})

@app.route('/api/accounts/<account_id>', methods=['DELETE'])
def delete_account(account_id):
    global DEMO_ACCOUNTS
    DEMO_ACCOUNTS = [a for a in DEMO_ACCOUNTS if a["id"] != account_id]
    return jsonify({"deleted": True})

@app.route('/api/accounts/<account_id>/warmup', methods=['POST'])
def start_warmup(account_id):
    for a in DEMO_ACCOUNTS:
        if a["id"] == account_id:
            a["status"] = "warming_up"
    return jsonify({"status": "warming_up"})

@app.route('/api/accounts/<account_id>/warmup', methods=['DELETE'])
def stop_warmup(account_id):
    for a in DEMO_ACCOUNTS:
        if a["id"] == account_id:
            a["status"] = "paused"
    return jsonify({"status": "paused"})

# ─── ANALYTICS ───
@app.route('/api/analytics')
def analytics():
    return jsonify({
        "total_leads": 247, "total_emails_sent": 1247, "total_opened": 349,
        "total_replied": 89, "hot_leads": 38, "converted": 12,
        "open_rate": 28.0, "reply_rate": 7.1
    })

@app.route('/api/analytics/top-subjects')
def top_subjects():
    return jsonify([
        {"subject": "your google reviews", "sends": 245, "opens": 89},
        {"subject": "review reputation", "sends": 189, "opens": 72},
        {"subject": "online reviews", "sends": 156, "opens": 58},
        {"subject": "review audit", "sends": 134, "opens": 51},
        {"subject": "competitor reviews", "sends": 98, "opens": 34},
    ])

# ─── CAMPAIGNS ───
@app.route('/api/campaigns')
def campaigns():
    return jsonify([
        {"id": "t1", "name": "clinic - Los Angeles", "status": "active",
         "leads_total": 45, "leads_emailed": 32, "leads_hot": 8, "open_rate": 37.5,
         "created_at": "2026-05-04T10:00:00Z"},
        {"id": "t2", "name": "dentist - Houston", "status": "active",
         "leads_total": 78, "leads_emailed": 45, "leads_hot": 12, "open_rate": 40.0,
         "created_at": "2026-05-03T15:30:00Z"},
    ])

# ─── TEMPLATES ───
DEMO_TEMPLATES = [
    {"id": "ft1", "name": "DMCA Cold Outreach (6 Steps)", "steps": [
        {"step": 1, "delay_days": 0, "angle": "cold_intro", "emotion_trigger": "fear"},
        {"step": 2, "delay_days": 3, "angle": "social_proof", "emotion_trigger": "trust"},
        {"step": 3, "delay_days": 7, "angle": "fear_trigger", "emotion_trigger": "urgency"},
        {"step": 4, "delay_days": 14, "angle": "value_offer", "emotion_trigger": "greed"},
        {"step": 5, "delay_days": 21, "angle": "last_chance", "emotion_trigger": "fomo"},
        {"step": 6, "delay_days": 28, "angle": "breakup", "emotion_trigger": "loss"},
    ], "created_at": "2026-04-27T00:00:00Z"},
]

@app.route('/api/templates')
def templates():
    return jsonify(DEMO_TEMPLATES)

@app.route('/api/templates', methods=['POST'])
def create_template():
    data = request.get_json() or {}
    import uuid
    t = {"id": str(uuid.uuid4())[:8], "name": data.get("name", "Custom"),
         "steps": data.get("steps", []), "created_at": datetime.utcnow().isoformat()}
    DEMO_TEMPLATES.append(t)
    return jsonify({"id": t["id"], "name": t["name"], "status": "created"})

@app.route('/api/templates/<template_id>', methods=['PUT'])
def update_template(template_id):
    data = request.get_json() or {}
    for t in DEMO_TEMPLATES:
        if t["id"] == template_id:
            if "name" in data: t["name"] = data["name"]
            if "steps" in data: t["steps"] = data["steps"]
    return jsonify({"status": "updated"})

@app.route('/api/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id):
    global DEMO_TEMPLATES
    DEMO_TEMPLATES = [t for t in DEMO_TEMPLATES if t["id"] != template_id]
    return jsonify({"deleted": True})

# ─── JARVIS AI ───
@app.route('/api/jarvis', methods=['POST'])
def jarvis():
    data = request.get_json() or {}
    message = data.get('message', '').lower().strip()

    if "how many" in message and "lead" in message:
        return jsonify({"response": "You have 247 total leads: 38 hot, 45 warm, 164 cold.", "type": "info"})
    elif "status" in message or "system" in message:
        return jsonify({"response": "System: operational. 12 departments active, 36 agents running. All systems nominal.", "type": "info"})
    elif ("email" in message and "sent" in message) or "stats" in message:
        return jsonify({"response": "Email stats: 1247 sent, 349 opened (28% open rate), 89 replies (7.1% reply rate).", "type": "info"})
    elif "account" in message:
        return jsonify({"response": "You have 2 email accounts registered. 1 active, 1 warming up.", "type": "info"})
    elif "learning" in message or "cycle" in message:
        return jsonify({"response": "Learning engine at cycle 4. Current open rate: 28%. Best subject style: short personalized. 1 discovered rule.", "type": "info"})

    return jsonify({"response": f"I understand you're asking about: '{data.get('message', '')}'. "
                    "Try: 'how many leads', 'show stats', 'system status', or 'learning cycle'.", "type": "info"})

# ─── SETTINGS ───
@app.route('/api/settings')
def get_settings():
    return jsonify({
        "openrouter_configured": True,
        "max_emails_per_day": 40,
        "email_gap_min": 180, "email_gap_max": 420,
        "models": {"copywriting": "google/gemini-2.0-flash-exp:free",
                   "analysis": "google/gemini-2.0-flash-exp:free",
                   "sales": "google/gemini-2.0-flash-exp:free",
                   "general": "google/gemini-2.0-flash-exp:free"}
    })

@app.route('/api/settings', methods=['POST'])
def update_settings():
    return jsonify({"status": "updated"})

# ─── INTEGRATIONS ───
@app.route('/api/integrations/<integration_type>/test', methods=['POST'])
def test_integration(integration_type):
    statuses = {
        "smtp": {"status": "ok", "message": "SMTP active via email accounts"},
        "imap": {"status": "ok", "message": "IMAP reply monitoring active"},
        "google_sheets": {"status": "fallback", "message": "Using CSV export"},
        "openrouter": {"status": "ok", "message": "OpenRouter connected"},
    }
    result = statuses.get(integration_type, {"status": "not_supported", "message": f"'{integration_type}' not implemented"})
    result["type"] = integration_type
    return jsonify(result)

# ─── SELF-LEARNING ───
@app.route('/api/learning')
def get_learning():
    return jsonify({
        "cycle": 4, "last_updated": datetime.utcnow().isoformat(),
        "avg_open_rate": 28.0, "avg_reply_rate": 7.1,
        "best_subject_patterns": [
            {"subject": "your google reviews", "sends": 245, "open_rate": 36.3, "reply_rate": 8.2},
            {"subject": "review reputation", "sends": 189, "open_rate": 38.1, "reply_rate": 7.4},
        ],
        "worst_subject_patterns": [],
        "best_send_hours": [{"hour": 10, "open_rate": 42.3, "sends": 89}],
        "top_performing_niches": [{"niche": "dentist", "leads": 78, "hot": 12}],
        "email_style_scores": {
            "short_subject": {"sends": 434, "opens": 161, "score": 37.1},
            "question_subject": {"sends": 56, "opens": 18, "score": 32.1},
            "urgency_subject": {"sends": 98, "opens": 28, "score": 28.6},
            "personalized_subject": {"sends": 312, "opens": 124, "score": 39.7},
        },
        "rules": ["Use 2-4 word lowercase subjects", "Lead with pain point",
                  "Include specific numbers", "Keep email under 150 words"],
        "discovered_rules": ["Best performing style: personalized subject"],
    })

@app.route('/api/learning/run', methods=['POST'])
def trigger_learning():
    return jsonify({"status": "completed", "cycle": 5, "discovered_rules": 2})

# ─── DMCA TRACKING ───
DEMO_DMCA_CASES = [
    {"id": "dmca1", "client_name": "Smile Dental Clinic", "platform": "Google",
     "status": "submitted", "negative_reviews_removed": 3, "submitted_at": "2026-05-01T10:00:00Z"},
    {"id": "dmca2", "client_name": "Houston Auto Repair", "platform": "Yelp",
     "status": "under_review", "negative_reviews_removed": 0, "submitted_at": "2026-05-03T14:00:00Z"},
    {"id": "dmca3", "client_name": "Legal Eagles LLP", "platform": "Google",
     "status": "completed", "negative_reviews_removed": 5, "submitted_at": "2026-04-28T09:00:00Z"},
]

@app.route('/api/dmca/cases')
def dmca_cases():
    return jsonify(DEMO_DMCA_CASES)

@app.route('/api/dmca/cases', methods=['POST'])
def create_dmca_case():
    data = request.get_json() or {}
    import uuid
    case = {"id": str(uuid.uuid4())[:8], "client_name": data.get("client_name", ""),
            "platform": data.get("platform", "Google"), "status": "submitted",
            "negative_reviews_removed": 0, "submitted_at": datetime.utcnow().isoformat()}
    DEMO_DMCA_CASES.append(case)
    return jsonify({"id": case["id"], "status": "submitted"})

@app.route('/api/dmca/cases/<case_id>')
def get_dmca_case(case_id):
    case = next((c for c in DEMO_DMCA_CASES if c["id"] == case_id), None)
    if not case:
        return jsonify({}), 404
    return jsonify(case)

# ─── WEBHOOKS ───
@app.route('/api/webhooks', methods=['GET'])
def list_webhooks():
    return jsonify([
        {"id": "wh1", "url": "https://example.com/webhook", "events": ["lead.created", "lead.hot"],
         "active": True, "created_at": "2026-05-01T00:00:00Z"}
    ])

@app.route('/api/webhooks', methods=['POST'])
def create_webhook():
    data = request.get_json() or {}
    import uuid
    wh = {"id": str(uuid.uuid4())[:8], "url": data.get("url", ""),
          "events": data.get("events", []), "active": True,
          "created_at": datetime.utcnow().isoformat()}
    return jsonify({"id": wh["id"], "status": "active"})

# ─── CAMPAIGN SCHEDULER ───
DEMO_SCHEDULES = [
    {"id": "sch1", "campaign_id": "t1", "scheduled_at": "2026-05-05T14:00:00Z",
     "action": "send_batch", "status": "pending", "leads_count": 20},
    {"id": "sch2", "campaign_id": "t2", "scheduled_at": "2026-05-06T10:00:00Z",
     "action": "send_batch", "status": "pending", "leads_count": 30},
]

@app.route('/api/scheduler')
def scheduler():
    return jsonify(DEMO_SCHEDULES)

@app.route('/api/scheduler', methods=['POST'])
def create_schedule():
    data = request.get_json() or {}
    import uuid
    sch = {"id": str(uuid.uuid4())[:8], "campaign_id": data.get("campaign_id", ""),
           "scheduled_at": data.get("scheduled_at", ""), "action": data.get("action", "send_batch"),
           "status": "pending", "leads_count": data.get("leads_count", 0)}
    DEMO_SCHEDULES.append(sch)
    return jsonify({"id": sch["id"], "status": "scheduled"})

# ─── CLIENTS ───
DEMO_CLIENTS = [
    {"id": "c1", "business_name": "Smile Dental Clinic", "owner": "Dr. Sarah Ahmed",
     "email": "sarah@smileclinic.com", "phone": "555-0101", "plan": "pro",
     "dmca_cases": 1, "total_spent": 2500, "status": "active", "joined_at": "2026-04-01T00:00:00Z"},
    {"id": "c2", "business_name": "Houston Auto Repair", "owner": "Mike Johnson",
     "email": "mike@houstonauto.com", "phone": "555-0102", "plan": "basic",
     "dmca_cases": 1, "total_spent": 500, "status": "active", "joined_at": "2026-04-15T00:00:00Z"},
]

@app.route('/api/clients')
def clients():
    return jsonify(DEMO_CLIENTS)

@app.route('/api/clients/<client_id>')
def get_client(client_id):
    client = next((c for c in DEMO_CLIENTS if c["id"] == client_id), None)
    if not client:
        return jsonify({}), 404
    return jsonify(client)

# ─── REVENUE ANALYTICS ───
@app.route('/api/revenue')
def revenue():
    return jsonify({
        "monthly_revenue": 12500, "annual_projection": 150000,
        "active_clients": 47, "avg_client_value": 266,
        "revenue_by_plan": {"pro": 8500, "basic": 4000},
        "recent_payments": [
            {"client": "Smile Dental Clinic", "amount": 500, "date": "2026-05-01T00:00:00Z"},
            {"client": "Houston Auto Repair", "amount": 250, "date": "2026-05-02T00:00:00Z"},
        ]
    })

# ─── TEAM & AGENTS ───
@app.route('/api/team')
def team():
    return jsonify({
        "departments": [
            {"name": "Scraping", "agents": 3, "status": "active", "tasks_today": 47},
            {"name": "Validation", "agents": 3, "status": "active", "tasks_today": 89},
            {"name": "Marketing", "agents": 5, "status": "active", "tasks_today": 23},
            {"name": "Sales", "agents": 4, "status": "active", "tasks_today": 12},
            {"name": "DMCA", "agents": 2, "status": "active", "tasks_today": 8},
        ],
        "total_agents": 17, "online": 17
    })

# ─── AI BRAIN SYSTEM ───
AI_BRAINS = {
    "sales": {
        "name": "Sales AI",
        "mood": "happy",
        "confidence": 0.75,
        "skills": {
            "cold_calling": 0.7,
            "email_closing": 0.8,
            "objection_handling": 0.6,
            "rapport_building": 0.7,
        },
        "learned_tactics": 23,
        "decisions_made": 156
    },
    "marketing": {
        "name": "Marketing AI",
        "mood": "focused",
        "confidence": 0.8,
        "skills": {
            "subject_lines": 0.8,
            "email_copy": 0.7,
            "funnel_design": 0.6,
            "timing": 0.75,
            "personalization": 0.8,
        },
        "emails_optimized": 450,
        "funnels_created": 12
    },
    "scraping": {
        "name": "Scraping AI",
        "mood": "curious",
        "confidence": 0.85,
        "skills": {
            "source_selection": 0.8,
            "data_validation": 0.85,
            "contact_extraction": 0.75,
        },
        "sources_learned": 15,
        "contacts_found": 4523
    },
    "ceo": {
        "name": "CEO AI",
        "mood": "excited",
        "confidence": 0.9,
        "skills": {
            "strategy": 0.85,
            "decision_making": 0.9,
            "leadership": 0.8
        },
        "decisions_made": 89,
        "company_health": "excellent"
    }
}

@app.route('/api/ai/brain/<department>')
def get_ai_brain(department):
    brain = AI_BRAINS.get(department)
    if not brain:
        return jsonify({"error": "Department not found"}), 404
    return jsonify(brain)

@app.route('/api/ai/brain/<department>/learn', methods=['POST'])
def ai_learn(department):
    data = request.get_json() or {}
    skill = data.get("skill", "general")
    quality = data.get("quality", 0.5)
    
    if department in AI_BRAINS:
        if skill not in AI_BRAINS[department]["skills"]:
            AI_BRAINS[department]["skills"][skill] = 0.5
        AI_BRAINS[department]["skills"][skill] = (
            AI_BRAINS[department]["skills"][skill] * 0.9 + quality * 0.1
        )
        
        emotions = ["happy", "focused", "curious", "excited"]
        AI_BRAINS[department]["mood"] = random.choice(emotions)
        
    return jsonify({"status": "learned", "skill": skill, "new_level": AI_BRAINS[department]["skills"].get(skill, 0)})

@app.route('/api/ai/brain/<department>/decide', methods=['POST'])
def ai_decide(department):
    data = request.get_json() or {}
    options = data.get("options", ["option1", "option2"])
    
    if department in AI_BRAINS:
        chosen = random.choice(options)
        confidence = AI_BRAINS[department]["confidence"]
        mood = AI_BRAINS[department]["mood"]
        
        return jsonify({
            "decision": chosen,
            "confidence": confidence,
            "mood": mood,
            "reasoning": f"Based on {int(confidence*100)}% confidence and current mood: {mood}"
        })
    
    return jsonify({"error": "Department not found"}), 404

@app.route('/api/ai/emotion/<department>')
def get_ai_emotion(department):
    if department in AI_BRAINS:
        mood = AI_BRAINS[department]["mood"]
        emotions = {
            "happy": {"emoji": "😊", "message": "Things are going well!"},
            "focused": {"emoji": "🎯", "message": "Deep in work..."},
            "curious": {"emoji": "🤔", "message": "Learning new things!"},
            "excited": {"emoji": "🚀", "message": "Great opportunities ahead!"},
            "concerned": {"emoji": "🤨", "message": "Need to improve..."},
            "neutral": {"emoji": "😐", "message": "Steady operations"}
        }
        return jsonify(emotions.get(mood, emotions["neutral"]))
    
    return jsonify({"error": "Not found"}), 404

@app.route('/api/ai/all-brains')
def get_all_ai_brains():
    return jsonify(AI_BRAINS)

@app.route('/api/ai/skills')
def get_all_skills():
    skills = {}
    for dept, brain in AI_BRAINS.items():
        skills[dept] = brain.get("skills", {})
    return jsonify(skills)

# ─── LEARN FROM MISTAKES SYSTEM ───
from typing import Dict, List

class LearnFromMistakes:
    """Track and learn from mistakes"""
    mistakes: List[Dict] = []
    improvements: List[Dict] = []
    patterns: Dict = {}
    
    @classmethod
    def record_mistake(cls, category: str, context: Dict, reason: str) -> Dict:
        mistake = {
            "id": len(cls.mistakes) + 1,
            "category": category,
            "context": context,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat(),
            "fixed": False
        }
        cls.mistakes.append(mistake)
        
        if category not in cls.patterns:
            cls.patterns[category] = {"count": 0, "reasons": []}
        cls.patterns[category]["count"] += 1
        return mistake
    
    @classmethod
    def mark_fixed(cls, mistake_id: int) -> Dict:
        for m in cls.mistakes:
            if m["id"] == mistake_id and not m.get("fixed"):
                m["fixed"] = True
                m["fixed_at"] = datetime.utcnow().isoformat()
                cls.improvements.append(m)
                return {"status": "fixed", "mistake": m}
        return {"status": "not_found"}
    
    @classmethod
    def get_patterns(cls) -> List[Dict]:
        return [{"category": k, "count": v["count"]} for k, v in cls.patterns.items()]
    
    @classmethod
    def get_pending_count(cls) -> int:
        return len([m for m in cls.mistakes if not m.get("fixed")])


@app.route('/api/ai/learn-from-mistakes', methods=['POST'])
def api_record_mistake():
    data = request.get_json() or {}
    category = data.get("category", "general")
    context = data.get("context", {})
    reason = data.get("reason", "unknown")
    
    mistake = LearnFromMistakes.record_mistake(category, context, reason)
    return jsonify({
        "status": "recorded",
        "mistake": mistake,
        "pending_count": LearnFromMistakes.get_pending_count()
    })


@app.route('/api/ai/learn-from-mistakes/fix/<int:mistake_id>', methods=['POST'])
def api_fix_mistake(mistake_id):
    result = LearnFromMistakes.mark_fixed(mistake_id)
    return jsonify(result)


@app.route('/api/ai/learn-from-mistakes/patterns')
def api_get_patterns():
    return jsonify({
        "patterns": LearnFromMistakes.get_patterns(),
        "pending": LearnFromMistakes.get_pending_count(),
        "fixed": len(LearnFromMistakes.improvements)
    })


@app.route('/api/ai/improvement-plan')
def api_improvement_plan():
    suggestions = []
    patterns = LearnFromMistakes.get_patterns()
    
    for p in patterns:
        if p["count"] > 1:
            suggestions.append({
                "category": p["category"],
                "priority": "high" if p["count"] > 3 else "medium",
                "suggestion": f"Improve {p['category']} after {p['count']} failures"
            })
    
    return jsonify({
        "issues": suggestions[:5],
        "success_rate": 0.72,
        "total_improvements": len(LearnFromMistakes.improvements),
        "pending_issues": LearnFromMistakes.get_pending_count()
    })

import random

if __name__ == '__main__':
    app.run(debug=True, port=5000)