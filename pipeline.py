import re, time
from typing import List, Dict
from .models import *

COMMON_FEATURES = {
    'login': 'authentication', 'auth': 'authentication', 'dashboard': 'dashboard',
    'payment': 'payments', 'premium': 'premium_plan', 'analytics': 'analytics',
    'role': 'role_based_access', 'admin': 'admin_panel', 'crud': 'crud'
}

ENTITY_HINTS = {
    'crm': ['User', 'Contact', 'Plan'],
    'ecommerce': ['User', 'Product', 'Order', 'Payment'],
    'task': ['User', 'Task', 'Project'],
    'blog': ['User', 'Post', 'Comment'],
    'booking': ['User', 'Booking', 'Service']
}

class AppCompiler:
    def compile(self, prompt: str) -> CompileResponse:
        start = time.time()
        repair_attempts = 0
        intent = self.extract_intent(prompt)
        arch = self.design_system(intent)
        config = self.generate_schema(arch)
        issues = validate_config(config)
        while any(i.severity == 'error' for i in issues) and repair_attempts < 3:
            config = repair_config(config, issues)
            repair_attempts += 1
            issues = validate_config(config)
        html = simulate_runtime(config)
        metrics = {
            'latency_ms': round((time.time() - start) * 1000, 2),
            'error_count': len([i for i in issues if i.severity == 'error']),
            'warning_count': len([i for i in issues if i.severity == 'warning']),
            'repair_attempts': repair_attempts,
            'success': not any(i.severity == 'error' for i in issues)
        }
        return CompileResponse(
            intent=intent, architecture=arch, config=config,
            validation_issues=issues, repair_attempts=repair_attempts,
            executable_preview_html=html, metrics=metrics
        )

    def extract_intent(self, prompt: str) -> Intent:
        text = prompt.lower()
        app_type = 'general_app'
        for key in ENTITY_HINTS:
            if key in text:
                app_type = key
                break
        features = sorted({v for k, v in COMMON_FEATURES.items() if k in text})
        if not features:
            features = ['crud']
        roles = ['user']
        if 'admin' in text or 'role' in text:
            roles.append('admin')
        if 'manager' in text:
            roles.append('manager')
        entities = ENTITY_HINTS.get(app_type, ['User', 'Item'])
        # Extract simple custom entities after words like contacts/tasks/products
        for word in re.findall(r'\b(contacts|tasks|products|orders|bookings|projects)\b', text):
            ent = word[:-1].capitalize()
            if ent not in entities:
                entities.append(ent)
        assumptions = []
        if 'payment' in text or 'premium' in text:
            assumptions.append('Payments are represented as schema and gating logic only; no real payment gateway is integrated.')
        if 'login' in text or 'auth' in text:
            assumptions.append('Email/password authentication is assumed.')
        return Intent(app_type=app_type, features=features, roles=roles, entities=entities, assumptions=assumptions)

    def design_system(self, intent: Intent) -> Architecture:
        entities = []
        for e in intent.entities:
            fields = [EntityField(name='id', type='string'), EntityField(name='created_at', type='datetime')]
            if e == 'User':
                fields += [EntityField(name='email', type='string'), EntityField(name='role', type='string')]
            elif e == 'Contact':
                fields += [EntityField(name='name', type='string'), EntityField(name='email', type='string'), EntityField(name='phone', type='string', required=False)]
            elif e == 'Plan':
                fields += [EntityField(name='name', type='string'), EntityField(name='price', type='float'), EntityField(name='is_premium', type='boolean')]
            else:
                fields += [EntityField(name='title', type='string'), EntityField(name='description', type='text', required=False)]
            entities.append(Entity(name=e, fields=fields))
        pages = [Page(name='Login', route='/login', components=['form'], allowed_roles=['guest'])]
        pages.append(Page(name='Dashboard', route='/dashboard', components=['cards', 'table'], allowed_roles=intent.roles))
        for e in entities:
            if e.name != 'User':
                pages.append(Page(name=f'{e.name} Management', route=f'/{e.name.lower()}s', components=['table','form'], allowed_roles=intent.roles))
        if 'analytics' in intent.features:
            pages.append(Page(name='Analytics', route='/analytics', components=['chart','metric_cards'], allowed_roles=['admin'] if 'admin' in intent.roles else intent.roles))
        business = []
        if 'premium_plan' in intent.features:
            business.append('Premium-only features require a user with an active premium plan.')
        if 'role_based_access' in intent.features:
            business.append('Admin role can access analytics and all management pages; user role has limited CRUD access.')
        return Architecture(app_name='GeneratedApp', entities=entities, pages=pages, roles=intent.roles, business_rules=business, assumptions=intent.assumptions)

    def generate_schema(self, arch: Architecture) -> AppConfig:
        db = [DBTable(name=e.name.lower() + 's', fields=e.fields) for e in arch.entities]
        api = []
        for e in arch.entities:
            base = '/' + e.name.lower() + 's'
            fields = [f.name for f in e.fields]
            api += [
                APIEndpoint(path=base, method='GET', entity=e.name, required_role='user', response_fields=fields),
                APIEndpoint(path=base, method='POST', entity=e.name, required_role='user', request_fields=fields, response_fields=fields),
                APIEndpoint(path=base + '/{id}', method='PUT', entity=e.name, required_role='user', request_fields=fields, response_fields=fields),
                APIEndpoint(path=base + '/{id}', method='DELETE', entity=e.name, required_role='admin' if 'admin' in arch.roles else 'user')
            ]
        ui = []
        for p in arch.pages:
            for comp in p.components:
                api_map = None
                fields = []
                for e in arch.entities:
                    if e.name.lower() in p.route:
                        api_map = '/' + e.name.lower() + 's'
                        fields = [f.name for f in e.fields]
                ui.append(UIComponent(page=p.name, component_type=comp, maps_to_api=api_map, fields=fields))
        auth = [AuthRule(role=r, permissions=['read', 'create', 'update'] + (['delete','analytics'] if r == 'admin' else [])) for r in arch.roles]
        return AppConfig(app_name=arch.app_name, db_schema=db, api_schema=api, ui_schema=ui, auth_rules=auth, business_logic=arch.business_rules, assumptions=arch.assumptions)

def validate_config(config: AppConfig) -> List[ValidationIssue]:
    issues = []
    table_map = {t.name.lower().rstrip("s"): t for t in config.db_schema}
    roles = {r.role for r in config.auth_rules}
    api_paths = {a.path for a in config.api_schema}
    for api in config.api_schema:
        key = api.entity.lower().rstrip("s")
        if key not in table_map:
            issues.append(ValidationIssue(severity='error', layer='api-db', message=f'API entity {api.entity} has no DB table.', repair_hint='create_missing_table'))
            continue
        db_fields = {f.name for f in table_map[key].fields}
        for f in api.request_fields + api.response_fields:
            if f not in db_fields:
                issues.append(ValidationIssue(severity='error', layer='api-db', message=f'API field {f} not found in DB table for {api.entity}.', repair_hint='remove_or_add_field'))
        if api.required_role not in roles:
            issues.append(ValidationIssue(severity='error', layer='auth', message=f'Role {api.required_role} missing in auth rules.', repair_hint='add_role'))
    for ui in config.ui_schema:
        if ui.maps_to_api and ui.maps_to_api not in api_paths:
            issues.append(ValidationIssue(severity='error', layer='ui-api', message=f'UI component maps to missing API {ui.maps_to_api}.', repair_hint='fix_ui_mapping'))
    if not config.db_schema:
        issues.append(ValidationIssue(severity='error', layer='db', message='No database schema generated.'))
    return issues

def repair_config(config: AppConfig, issues: List[ValidationIssue]) -> AppConfig:
    roles = {r.role for r in config.auth_rules}
    for issue in issues:
        if issue.repair_hint == 'add_role':
            missing = issue.message.split('Role ')[1].split(' missing')[0]
            if missing not in roles:
                config.auth_rules.append(AuthRule(role=missing, permissions=['read']))
                roles.add(missing)
        if issue.repair_hint == 'fix_ui_mapping':
            valid_paths = {a.path for a in config.api_schema}
            for ui in config.ui_schema:
                if ui.maps_to_api and ui.maps_to_api not in valid_paths:
                    ui.maps_to_api = None
                    ui.fields = []
    return config

def simulate_runtime(config: AppConfig) -> str:
    nav = ''.join(f'<li>{ui.page} - {ui.component_type}</li>' for ui in config.ui_schema[:12])
    tables = ''.join(f'<h3>{t.name}</h3><p>{", ".join(f.name+":"+f.type for f in t.fields)}</p>' for t in config.db_schema)
    return f'''
    <html><body style="font-family:Arial;padding:24px">
    <h1>{config.app_name}</h1>
    <h2>Executable Preview</h2>
    <ul>{nav}</ul>
    <h2>Database</h2>{tables}
    </body></html>
    '''
