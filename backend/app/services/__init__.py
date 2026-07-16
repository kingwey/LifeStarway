from app.services.auth_service import register, login
from app.services.profile_service import get_profile, create_or_update_profile, import_resume, get_profile_versions
from app.services.plan_service import create_diagnosis, get_latest_diagnosis, get_diagnoses, get_diagnoses_count, generate_plan, get_plans, get_plans_count, get_plan
from app.services.starmap_service import get_starmap_data
from app.services.whatif_service import create_simulation, get_simulation, get_simulations
from app.services.scraper_service import import_from_public_sources
