COURSE_FORM_LAYOUT = [

    # =========================
    # 🔷 BASIC INFORMATION
    # =========================
    ("Basic Information", [
        "title",
        "code",
        "description",
        "status",
    ]),

    # =========================
    # 🔷 ACADEMIC STRUCTURE
    # =========================
    ("Academic Structure", [
        "level",
        "entry_qualification",
        "curriculum_category",
        "curriculum_availability",
        "equivalent_course",
        "industry",
        "ncs",   # 🔥 FK belongs here (not NVQ section)
    ]),

    # =========================
    # 🔷 DELIVERY SETTINGS
    # =========================
    ("Delivery", [
        "delivery_mode",
        "course_mode",
        "medium",
        "physical_resources",   # 🔥 ManyToMany (multi-select)
    ]),

    # =========================
    # 🔷 DURATION & HOURS
    # =========================
    ("Duration & Hours", [
        "duration_months",
        "theory_hours",
        "practical_hours",
        "assignment_hours",
        "ojt_months",
    ]),

    # =========================
    # 🔷 CAPACITY
    # =========================
    ("Capacity", [
        "batches_per_year",
        "students_per_batch",
    ]),

    # =========================
    # 🔷 FINANCIAL
    # =========================
    ("Financial", [
        "is_free",        # 🔥 put first (logic control)
        "course_fee",
        "fee_includes",
    ]),

    # =========================
    # 🔷 RESOURCE DETAILS (TEXT)
    # =========================
    ("Resource Details", [
        "tools_available",
        "equipment_available",
        "machinery_available",
    ]),

    # =========================
    # 🔷 NVQ DETAILS
    # =========================
    ("NVQ Details", [
        "nvq_level",
        "qualification_code",
    ]),

    # =========================
    # 🔷 PEDAGOGY
    # =========================
    ("Pedagogy", [
        "prerequisite",
        "learning_outcomes",
    ]),
]

COURSE_FORM_LAYOUT = [

    # =========================
    # 🔷 BASIC INFORMATION
    # =========================
    ("Basic Information", [
        "title",
        "code",
        "description",
        "status",
    ]),

    # =========================
    # 🔷 ACADEMIC STRUCTURE
    # =========================
    ("Academic Structure", [
        "level",
        "entry_qualification",
        "curriculum_category",
        "curriculum_availability",
        "equivalent_course",
        "industry",
    ]),

    # =========================
    # 🔷 DELIVERY SETTINGS
    # =========================
    ("Delivery", [
        "delivery_mode",
        "course_mode",
        "medium",

    ]),

    # =========================
    # 🔷 DURATION & HOURS
    # =========================
    ("Duration & Hours", [
        "duration_months",
        "theory_hours",
        "practical_hours",
        "assignment_hours",
        "ojt_months",
    ]),

    # =========================
    # 🔷 CAPACITY
    # =========================
    ("Capacity", [
        "batches_per_year",
        "students_per_batch",
    ]),

    # =========================
    # 🔷 FINANCIAL
    # =========================
    ("Financial", [
        "course_fee",
        "is_free",
        "fee_includes",
    ]),

    # =========================
    # 🔷 PHYSICAL RESOURCES
    # =========================
    ("Physical Resources", [
        "tools_available",
        "equipment_available",
        "machinery_available",
            "physical_resources",]),

    # =========================
    # 🔷 NVQ DETAILS
    # =========================
    ("NVQ Details", [
        "nvq_level",
        "qualification_code",
        "ncs",
    ]),

    # =========================
    # 🔷 PEDAGOGY
    # =========================
    ("Pedagogy", [
        "prerequisite",
        "learning_outcomes",
    ]),

]


RELATION_LAYOUT = [
    {
        "name": "learning_resources",
        "label": "Learning Resources",
        "fields": ["name", "type", "file", "url", "description"],
    }
]
