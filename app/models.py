from typing import List, Dict, Literal, Optional, Any
from pydantic import BaseModel, Field

FieldType = Literal['string', 'integer', 'float', 'boolean', 'datetime', 'text']
HttpMethod = Literal['GET', 'POST', 'PUT', 'DELETE']

class Intent(BaseModel):
    app_name: str = 'GeneratedApp'
    app_type: str
    features: List[str] = Field(default_factory=list)
    roles: List[str] = Field(default_factory=lambda: ['user'])
    entities: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)

class EntityField(BaseModel):
    name: str
    type: FieldType
    required: bool = True

class Entity(BaseModel):
    name: str
    fields: List[EntityField]

class Page(BaseModel):
    name: str
    route: str
    components: List[str]
    allowed_roles: List[str]

class Architecture(BaseModel):
    app_name: str
    entities: List[Entity]
    pages: List[Page]
    roles: List[str]
    business_rules: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)

class DBTable(BaseModel):
    name: str
    fields: List[EntityField]

class APIEndpoint(BaseModel):
    path: str
    method: HttpMethod
    entity: str
    required_role: str
    request_fields: List[str] = Field(default_factory=list)
    response_fields: List[str] = Field(default_factory=list)

class UIComponent(BaseModel):
    page: str
    component_type: str
    maps_to_api: Optional[str] = None
    fields: List[str] = Field(default_factory=list)

class AuthRule(BaseModel):
    role: str
    permissions: List[str]

class AppConfig(BaseModel):
    app_name: str
    db_schema: List[DBTable]
    api_schema: List[APIEndpoint]
    ui_schema: List[UIComponent]
    auth_rules: List[AuthRule]
    business_logic: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)

class ValidationIssue(BaseModel):
    severity: Literal['error', 'warning']
    layer: str
    message: str
    repair_hint: Optional[str] = None

class CompileResponse(BaseModel):
    intent: Intent
    architecture: Architecture
    config: AppConfig
    validation_issues: List[ValidationIssue]
    repair_attempts: int
    executable_preview_html: str
    metrics: Dict[str, Any]
