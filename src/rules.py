import json
import os

# ─── Human-Readable Feature Labels ───────────────────────────────────────────
# Maps internal feature names → display labels shown in the frontend/API output.
FEATURE_LABELS = {
    'failures':          'Prior Class Failures',
    'studytime':         'Weekly Study Time',
    'absences':          'School Absences',
    'support_index':     'Support Network (School + Family + Aspiration)',
    'risk_behavior':     'Risk Behaviour Index (Alcohol + Social)',
    'Medu':              "Mother's Education Level",
    'Fedu':              "Father's Education Level",
    'higher':            'Aspiration for Higher Education',
    'goout':             'Frequency of Going Out with Friends',
    'Dalc':              'Workday Alcohol Consumption',
    'Walc':              'Weekend Alcohol Consumption',
    'famrel':            'Family Relationship Quality',
    'freetime':          'Free Time After School',
    'health':            'Current Health Status',
    'traveltime':        'Home-to-School Travel Time',
    'schoolsup':         'Extra Educational Support (School)',
    'famsup':            'Family Educational Support',
    'paid':              'Extra Paid Tutoring Classes',
    'internet':          'Internet Access at Home',
    'activities':        'Extracurricular Activities',
    'nursery':           'Attended Nursery School',
    'romantic':          'In a Romantic Relationship',
    'Pstatus_T':         "Parents' Cohabitation Status",
    'famsize_LE3':       'Family Size',
    'guardian_mother':   "Guardian (Mother)",
    'guardian_other':    "Guardian (Other)",
    'Mjob_health':       "Mother's Job (Healthcare)",
    'Mjob_other':        "Mother's Job (Other)",
    'Mjob_services':     "Mother's Job (Services)",
    'Mjob_teacher':      "Mother's Job (Teacher)",
    'Fjob_health':       "Father's Job (Healthcare)",
    'Fjob_other':        "Father's Job (Other)",
    'Fjob_services':     "Father's Job (Services)",
    'Fjob_teacher':      "Father's Job (Teacher)",
    'reason_home':       'School Choice Reason (Proximity to Home)',
    'reason_other':      'School Choice Reason (Other)',
    'reason_reputation': 'School Choice Reason (Reputation)',
    'subject_Portuguese':'Subject (Portuguese)',
}

# ─── Intervention Map ─────────────────────────────────────────────────────────
# Every feature that can surface as a SHAP top-driver must have a specific,
# real-world, actionable intervention here. No feature should produce the generic fallback.
INTERVENTION_MAP = {
    # ── Academic Performance & Behaviour ──
    'failures': (
        "ACADEMIC: Student has prior class failure(s) — the strongest single predictor of future failure. "
        "ACTION → Mandate immediate enrollment in a structured peer-tutoring or remedial support programme. "
        "Schedule bi-weekly check-ins with the form tutor to monitor progress."
    ),
    'studytime': (
        "HABIT: Low weekly study time detected (likely <2 hrs/week). "
        "ACTION → Enroll student in a 'Time Management & Study Skills' workshop. "
        "Assign a study buddy and set weekly minimum study hour targets tracked by the advisor."
    ),
    'absences': (
        "ATTENDANCE: High number of school absences recorded. "
        "ACTION → Trigger an automated academic advisor check-in within 48 hours. "
        "Draft an Attendance Improvement Contract and notify the guardian."
    ),
    'support_index': (
        "SUPPORT: Low composite support score (school support + family support + higher-education aspiration). "
        "ACTION → Connect student with the on-campus mentorship programme. "
        "Arrange a parent-teacher conference to align on academic expectations."
    ),
    'risk_behavior': (
        "LIFESTYLE: Elevated risk behaviour index (alcohol consumption + social going-out frequency). "
        "ACTION → Schedule a confidential wellness counselling session. "
        "Introduce student to structured after-school activities as a positive alternative."
    ),

    # ── Alcohol & Social ──
    'Dalc': (
        "LIFESTYLE: High workday alcohol consumption reported. "
        "ACTION → Refer to school counsellor for a confidential substance-use awareness session. "
        "Flag for welfare team follow-up."
    ),
    'Walc': (
        "LIFESTYLE: High weekend alcohol consumption reported. "
        "ACTION → Schedule a wellness check-in. Provide resources on student wellbeing support services."
    ),
    'goout': (
        "LIFESTYLE: High frequency of going out with friends is impacting study time. "
        "ACTION → Advisor discussion on balancing social life and academic responsibilities. "
        "Suggest a structured weekly schedule."
    ),
    'freetime': (
        "HABIT: Excessive unstructured free time is negatively correlated with performance. "
        "ACTION → Suggest enrollment in structured extracurricular activities, library study sessions, or a study group."
    ),

    # ── Parental & Family Factors ──
    'Medu': (
        "FAMILY: Low maternal education level — student may have limited academic support at home. "
        "ACTION → Connect student with school-provided homework assistance programmes and online tutoring resources."
    ),
    'Fedu': (
        "FAMILY: Low paternal education level — student may have limited academic support at home. "
        "ACTION → Ensure student is aware of all available school support resources and after-school tutoring."
    ),
    'famrel': (
        "FAMILY: Poor family relationship quality reported. "
        "ACTION → Refer student to pastoral care / school counsellor. Consider family liaison officer involvement."
    ),
    'famsup': (
        "SUPPORT: No family educational support at home. "
        "ACTION → Enroll student in school's after-hours study support programme. "
        "Provide guardian with guidance resources."
    ),
    'Pstatus_T': (
        "FAMILY: Parents are living apart — potential home instability factor. "
        "ACTION → Pastoral check-in to assess student's home environment and emotional wellbeing."
    ),
    'famsize_LE3': (
        "FAMILY: Small family size (≤3 members) — limited home support network. "
        "ACTION → Ensure student has access to peer mentoring or tutoring as a supplementary support system."
    ),
    'guardian_mother': (
        "FAMILY: Mother is sole guardian. "
        "ACTION → Ensure communication channels with guardian are active. Schedule a parent-advisor meeting."
    ),
    'guardian_other': (
        "FAMILY: Non-parental guardian. "
        "ACTION → Verify guardian is engaged with the student's academic progress. Schedule a welfare check."
    ),

    # ── Support & Resources ──
    'schoolsup': (
        "SUPPORT: Student is receiving extra school educational support — may indicate prior identified need. "
        "ACTION → Review the effectiveness of current support plan with the SENCO / support coordinator."
    ),
    'paid': (
        "SUPPORT: No extra paid tutoring classes. "
        "ACTION → Explore eligibility for school-funded tutoring or low-cost community tutoring programmes."
    ),
    'internet': (
        "RESOURCE: No internet access at home. "
        "ACTION → Provide student with library access card for after-school internet use. "
        "Share offline study materials or textbooks."
    ),
    'higher': (
        "ASPIRATION: Student does not aspire to higher education. "
        "ACTION → Arrange a careers guidance session to explore vocational and academic pathways. "
        "Assign a mentor who can demonstrate achievable positive outcomes."
    ),

    # ── Engagement & Lifestyle ──
    'activities': (
        "ENGAGEMENT: Student is not involved in extracurricular activities. "
        "ACTION → Encourage participation in clubs, sports, or volunteer programmes to build engagement and belonging."
    ),
    'romantic': (
        "LIFESTYLE: Student is in a romantic relationship that may be impacting study time. "
        "ACTION → Advisor pastoral check-in on time management and balancing personal and academic commitments."
    ),
    'health': (
        "WELLBEING: Poor current health status reported. "
        "ACTION → Refer to school nurse / health coordinator. Assess whether health is causing absences or concentration issues."
    ),

    # ── Logistical ──
    'traveltime': (
        "LOGISTICAL: Long home-to-school travel time (>30 min) — increases fatigue and risk of late arrival. "
        "ACTION → Explore eligibility for school transport support. Discuss with guardian."
    ),
    'nursery': (
        "BACKGROUND: Student did not attend nursery school — may indicate gaps in early foundational learning. "
        "ACTION → Assess for any lingering literacy/numeracy gaps via a diagnostic assessment."
    ),

    # ── Job / Reason Proxies ──
    'Mjob_other': (
        "FAMILY: Mother's job category ('other') — limited socioeconomic context. "
        "ACTION → Ensure student is connected to all available school support resources."
    ),
    'Mjob_services': (
        "FAMILY: Mother works in public services — may have irregular hours. "
        "ACTION → Confirm student has adequate home supervision and support during study hours."
    ),
    'Mjob_teacher': (
        "FAMILY: Mother is a teacher — generally positive educational environment. "
        "ACTION → Leverage parental engagement for co-designing a home study plan."
    ),
    'Mjob_health': (
        "FAMILY: Mother works in healthcare — may have irregular/long shifts affecting home support. "
        "ACTION → Ensure student is connected with school-side support to compensate for reduced home availability."
    ),
    'Fjob_other': (
        "FAMILY: Father's job category ('other') — limited socioeconomic context. "
        "ACTION → Ensure student is connected to all available school support resources."
    ),
    'Fjob_services': (
        "FAMILY: Father works in public services. "
        "ACTION → Confirm student has adequate home supervision and support during study hours."
    ),
    'Fjob_teacher': (
        "FAMILY: Father is a teacher — generally positive educational environment. "
        "ACTION → Leverage parental engagement for co-designing a home study plan."
    ),
    'Fjob_health': (
        "FAMILY: Father works in healthcare — may have irregular/long shifts. "
        "ACTION → Ensure student is connected with school-side support to compensate."
    ),
    'reason_home': (
        "ENGAGEMENT: Student chose this school purely due to proximity, not academic preference. "
        "ACTION → Advisor session to explore student's academic interests and build motivation."
    ),
    'reason_other': (
        "ENGAGEMENT: School was chosen for unspecified reasons — may indicate low academic motivation. "
        "ACTION → Careers guidance session to help student connect current study with future goals."
    ),
    'reason_reputation': (
        "ENGAGEMENT: Student chose school for its reputation — may have high expectations with low preparation. "
        "ACTION → Academic review to ensure student is keeping pace with cohort standards."
    ),
    'subject_Portuguese': (
        "ACADEMIC: Risk profile relates to the Portuguese language subject. "
        "ACTION → Arrange subject-specific tutoring session. Review past assessment feedback with subject teacher."
    ),
}


def get_intervention(feature_name):
    """Returns the mapped intervention action or a safe default."""
    return INTERVENTION_MAP.get(
        feature_name,
        f"GENERAL: Discuss the impact of '{get_label(feature_name)}' during the next advising session."
    )


def get_label(feature_name):
    """Returns the human-readable display label for a feature."""
    return FEATURE_LABELS.get(feature_name, feature_name.replace('_', ' ').title())