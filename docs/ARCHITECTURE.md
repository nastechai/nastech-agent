# NasTech Branding System Architecture

## System Overview

The NasTech Branding System is a **multi-stage, multi-language, production-grade** transformation pipeline that handles branding changes across 40+ ecosystems and 150+ file types.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Branding Orchestrator                         │
│                  (branding-orchestrator.sh)                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐        ┌─────────┐      ┌──────────┐
   │ Content │        │  File   │      │ Registry │
   │Transform│        │Renaming │      │ Tracking │
   └─────────┘        └─────────┘      └──────────┘
        │
        ├─────────────────┬─────────────────┬──────────────────┐
        │                 │                 │                  │
        ▼                 ▼                 ▼                  ▼
   ┌──────────┐      ┌──────────┐    ┌──────────┐      ┌──────────┐
   │  Python  │      │ Node.js  │    │  Docker  │      │   YAML   │
   │  Engine  │      │Validator │    │Validator │      │Validator │
   └──────────┘      └──────────┘    └──────────┘      └──────────┘
        │                 │                 │                  │
        ├─────────────────┼─────────────────┼──────────────────┤
        │                 │                 │                  │
        ▼                 ▼                 ▼                  ▼
   ┌──────────────────────────────────────────────────────────────┐
   │         Ecosystem Validators (40+ ecosystems)                 │
   │  Python │ Node.js │ Go │ Rust │ Java │ Ruby │ PHP │ .NET    │
   │  Kotlin │ Scala │ Clojure │ Elixir │ Haskell │ R │ Perl     │
   │  Swift │ Build Systems │ CI/CD │ Infrastructure │ Web        │
   └──────────────────────────────────────────────────────────────┘
        │
        ▼
   ┌──────────────────────────────────────────────────────────────┐
   │              Final Verification & Reporting                   │
   │  - Residual reference checks                                  │
   │  - Compliance validation                                      │
   │  - Git diff summary                                           │
   │  - Metrics and statistics                                     │
   └──────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Orchestrator Layer

**File**: `branding-orchestrator.sh`  
**Language**: Bash  
**Role**: Master coordinator

```bash
# Responsibilities
- Validate repository state
- Sequence all phases
- Handle parallel/sequential execution
- Aggregate results
- Generate final report
- Manage logging

# Execution Modes
- transform: Apply all transformations
- validate: Check compliance only
- report: Generate detailed report
```

### 2. Core Transformation Engine

**File**: `branding_engine.py`  
**Language**: Python 3  
**Role**: Content transformation and file processing

```python
# Components
- BrandingRule: Single transformation rule with priority
- BrandingRules: Database of all rules (sorted by priority)
- FileTypeDetector: Identifies file types and skip patterns
- ContentTransformer: Applies rules to different file formats
- FileProcessor: Processes individual files
- FileRenamer: Renames files/directories
- BrandingValidator: Validates compliance
```

**Key Features**:
- AST-aware transformations
- Safe regex escaping
- Format preservation (JSON, YAML, etc.)
- Dry-run support
- Comprehensive error handling

### 3. npm Ecosystem Validator

**File**: `validate-npm-branding.js`  
**Language**: Node.js  
**Role**: npm/package manager ecosystem validation

```javascript
// Validates
- package.json (name, dependencies, scopes)
- package-lock.json (locked versions)
- yarn.lock (Yarn dependencies)
- pnpm-lock.yaml (pnpm dependencies)
- .npmrc (npm configuration)
- .yarnrc (Yarn configuration)

// Checks
- Package names containing "nastech"
- @nastech-research scope usage
- Repository URLs
- Monorepo workspaces
```

### 4. Docker Ecosystem Validator

**File**: `validate-docker-branding.sh`  
**Language**: Bash  
**Role**: Docker/container ecosystem validation

```bash
# Validates
- Dockerfile (base images, env vars, paths)
- docker-compose.yml (services, images)
- .dockerignore (patterns)
- GitHub Actions (Docker steps)
- Registry configuration
- Build scripts

# Checks
- nastechairesearch/nastech image references
- NASTECH_ environment variables
- /opt/nastech path references
- Docker registry URLs
```

### 5. Configuration Validator

**File**: `validate-config-branding.py`  
**Language**: Python 3  
**Role**: Configuration file validation

```python
# Validates
- YAML files (.yml, .yaml)
- TOML files (.toml)
- INI files (.ini, .conf, .config)
- Environment files (.env, .env.*)
- JSON files (.json)
- Markdown files (.md)

# Features
- Structured parsing (preserves format)
- Recursive object transformation
- Safe replacements
```

### 6. Ecosystem Validator (40+)

**File**: `validate-ecosystem-branding.py`  
**Language**: Python 3  
**Role**: Multi-ecosystem validation

```python
# Supported Ecosystems
- Python (setup.py, pyproject.toml, requirements.txt, etc.)
- Node.js (package.json, yarn.lock, pnpm-lock.yaml, etc.)
- Go (go.mod, go.sum, *.go)
- Rust (Cargo.toml, Cargo.lock)
- Java (pom.xml, build.gradle, settings.gradle)
- Ruby (Gemfile, Gemfile.lock)
- PHP (composer.json, composer.lock)
- .NET (.csproj, .fsproj, packages.config)
- Kotlin, Scala, Clojure, Elixir, Haskell, R, Perl, Swift
- Build Systems (Make, CMake, Bazel, Maven, Gradle, SBT, Ant)
- CI/CD (GitHub Actions, GitLab CI, CircleCI, Jenkins, Travis, Azure)
- Infrastructure (Docker, Kubernetes, Terraform, Ansible, Helm)
- Web (HTML, CSS, JavaScript, TypeScript, Vue, React)
- Documentation (Markdown, README)
- Configuration (YAML, TOML, JSON, INI, .env)

# Features
- Ecosystem-specific file pattern matching
- Context-aware rule application
- Parallel processing support
```

---

## Data Flow

### Transformation Flow

```
Input Repository
    │
    ├─→ [Phase 1] Content Transformation
    │   ├─→ Read file content
    │   ├─→ Apply branding rules (priority-ordered)
    │   ├─→ Preserve format (JSON, YAML, etc.)
    │   └─→ Write back to file
    │
    ├─→ [Phase 2] File/Directory Renaming
    │   ├─→ Find all files/dirs with "nastech" in name
    │   ├─→ Rename deepest-first (avoid broken paths)
    │   └─→ Update references in content
    │
    ├─→ [Phase 3] npm Validation
    │   ├─→ Locate all package.json files
    │   ├─→ Check package names, scopes, dependencies
    │   └─→ Fix violations
    │
    ├─→ [Phase 4] Docker Validation
    │   ├─→ Locate Dockerfile, docker-compose.yml
    │   ├─→ Check image references, env vars
    │   └─→ Fix violations
    │
    ├─→ [Phase 5] Configuration Validation
    │   ├─→ Locate YAML, TOML, JSON, INI, .env files
    │   ├─→ Parse and validate structure
    │   └─→ Fix violations
    │
    ├─→ [Phase 6] Ecosystem Validation (40+)
    │   ├─→ Locate ecosystem-specific files
    │   ├─→ Apply ecosystem-specific rules
    │   └─→ Fix violations
    │
    └─→ [Phase 7] Final Verification
        ├─→ Check for residual references
        ├─→ Validate compliance
        ├─→ Generate report
        └─→ Output metrics
    │
    ▼
Transformed Repository
```

---

## Rule Engine

### Priority-Based Execution

Rules are sorted by **priority** (highest first) to prevent partial replacements:

```
Priority 100: github.com/nastechai/nastech-agent → github.com/nastechai/nastech-agent
Priority 95:  nastechairesearch/nastech → nastechairesearch/nastech
Priority 90:  NasTech Agent → NasTech Agent
Priority 90:  nastech-agent → nastech-agent
Priority 85:  @nastech-research → @nastech-research
Priority 80:  NasTech → NasTech
Priority 80:  nastechai → nastechai
Priority 80:  nastechairesearch → nastechairesearch
Priority 75:  NASTECH_ → NASTECH_
Priority 75:  /opt/nastech → /opt/nastech
Priority 75:  ~/.nastech → ~/.nastech
Priority 50:  NasTech → NasTech
Priority 50:  nastech → nastech
```

**Why Priority Matters**:
- Prevents `NasTech` from matching before `NasTech Agent`
- Ensures full URLs are replaced before partial matches
- Maintains semantic correctness

### Rule Application Algorithm

```python
def apply_rules(content, rules):
    result = content
    replacements = 0
    
    for rule in sorted(rules, by_priority_desc):
        old_text = rule.old_text
        new_text = rule.new_text
        
        # Count occurrences
        count = result.count(old_text)
        
        if count > 0:
            # Apply replacement
            result = result.replace(old_text, new_text)
            replacements += count
    
    return result, replacements
```

---

## File Type Handling

### Detection Strategy

```
File Extension → File Type → Parser → Transformer
    │
    ├─→ .py, .js, .ts → Code → Text → Safe replacement
    ├─→ .json → JSON → JSON parser → Structure-aware
    ├─→ .yml, .yaml → YAML → YAML parser → Structure-aware
    ├─→ .toml → TOML → TOML parser → Structure-aware
    ├─→ .xml → XML → XML parser → Structure-aware
    ├─→ .ini, .conf → INI → INI parser → Structure-aware
    ├─→ .md → Markdown → Text → Safe replacement
    ├─→ .sh, .bash → Shell → Text → Safe replacement
    └─→ Binary → Skip → N/A → N/A
```

### Binary Detection

```bash
# Method 1: Extension-based
if [[ "$file" == *.png || "$file" == *.jpg ]]; then
    skip_file
fi

# Method 2: Content-based
if grep -qI '' "$file"; then
    # Text file
else
    # Binary file
fi
```

---

## Error Handling

### Graceful Degradation

```
Error Scenario → Handling Strategy → Result
    │
    ├─→ File not readable → Log warning → Skip file
    ├─→ JSON parse error → Fall back to text → Continue
    ├─→ Permission denied → Log error → Skip file
    ├─→ Merge conflict → Abort workflow → Manual resolution
    ├─→ Missing dependency → Log warning → Skip validator
    └─→ Validation failure → Create issue → Continue
```

### Error Codes

```
0   - Success
1   - Validation failed (critical errors)
2   - File not found
3   - Permission denied
4   - Merge conflict
5   - Missing dependency
```

---

## Performance Optimization

### Parallel Execution

```bash
# Sequential (default)
run_validator_1
run_validator_2
run_validator_3

# Parallel (--parallel flag)
run_validator_1 &
run_validator_2 &
run_validator_3 &
wait $PID1 $PID2 $PID3
```

### File Deduplication

```python
# Prevent processing same file multiple times
seen_files = {}
for pattern in include_patterns:
    for file in glob(pattern):
        if file not in seen_files:
            seen_files[file] = True
            process(file)
```

### Caching

```python
# Cache file type detection
file_type_cache = {}
for file in files:
    if file not in file_type_cache:
        file_type_cache[file] = detect_type(file)
```

---

## Integration Points

### GitHub Actions

```yaml
# Workflow triggers
- schedule: Daily at 02:00 UTC
- push: When scripts change
- workflow_dispatch: Manual trigger
- repository_dispatch: Webhook from upstream

# Outputs
- PR to nastechai/nastech-agent
- Issue for failures
- Workflow logs
```

### Git Integration

```bash
# Commit message
git commit -m "chore: sync and rebrand from NasTech
Upstream: main@<sha>
Message: <commit message>
Automated by: NasTech Sync Bot"

# Diff tracking
git diff --stat
git log --oneline
```

---

## Extensibility

### Adding New Ecosystems

1. Define ecosystem in `validate-ecosystem-branding.py`:
```python
ECOSYSTEMS['my-lang'] = [
    EcosystemConfig('config.file', ['*.config'], 'text', 'my-lang'),
]
```

2. Add file patterns and parsing logic

3. Run validator:
```bash
python3 validate-ecosystem-branding.py --repo . --ecosystem my-lang
```

### Adding New Rules

1. Update `BRANDING_RULES` in any validator:
```python
BRANDING_RULES = [
    ('old_text', 'new_text', priority),
]
```

2. Ensure priority is correct (higher = applied first)

3. Test with `test-branding-system.sh`

---

## Metrics & Monitoring

### Collected Metrics

```
- Files scanned
- Files modified
- Total replacements
- Items renamed
- Violations found
- Transformations applied
- Execution time
- Success/failure status
```

### Log Output

```
/tmp/branding-orchestrator-YYYYMMDD-HHMMSS.log
├── Phase 1: Content Transformation
├── Phase 2: File/Directory Renaming
├── Phase 3: npm Validation
├── Phase 4: Docker Validation
├── Phase 5: Configuration Validation
├── Phase 6: Ecosystem Validation (40+)
├── Phase 7: Final Verification
└── Git Changes Summary
```

---

## Testing Strategy

### Unit Tests

- Individual validator tests
- Rule application tests
- File type detection tests

### Integration Tests

- Full transformation pipeline
- Multi-ecosystem validation
- Git integration

### Test Repository

```bash
# Create test repo with sample files
./test-branding-system.sh

# Verify all transformations
# Check for residual references
# Validate compliance
```

---

## Security Considerations

### Input Validation

- Verify git repository before processing
- Check file permissions before writing
- Validate JSON/YAML/XML before parsing

### Injection Prevention

- Escape regex special characters
- Sanitize template variables
- Use safe string replacement methods

### Access Control

- Require GitHub token for PR creation
- Use force-with-lease for safe pushes
- Validate webhook signatures

---

## Future Enhancements

- [ ] Support for additional ecosystems (Lua, Nim, Zig)
- [ ] Machine learning-based branding detection
- [ ] Real-time sync monitoring
- [ ] Advanced conflict resolution
- [ ] Custom rule definitions via config file
- [ ] Web UI for monitoring and control
- [ ] Distributed processing for large repos
- [ ] Integration with code review tools

---

## References

- [Branding Rules](./BRANDING_RULES.md)
- [API Reference](./API.md)
- [Examples](./EXAMPLES.md)
- [Troubleshooting](../README.md#-troubleshooting)
