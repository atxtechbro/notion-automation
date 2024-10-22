## [1.0.1] - 2024-10-22

### Chores

- Restructured repository to adhere to Python packaging standards.
- Moved `cli.py` and `notion_client` module into `notion_automation/` package.
- Added necessary `__init__.py` files to ensure proper package recognition.

# 1.0.0 (2024-10-21)

### Bug Fixes

- **cli:** correct EntryConfig instantiation using keyword arguments for properties ([b642841](https://github.com/atxtechbro/notion-automation/commit/b642841cbdca110e296febdd3db3694e0572e9bc))
- enhance schema parsing and error messages, ensuring all tests pass ([480ab62](https://github.com/atxtechbro/notion-automation/commit/480ab62e9f7af06412e414920335370d7c19cf8f))
- Handle empty tasks.json file in add_task_from_raw function ([d33d096](https://github.com/atxtechbro/notion-automation/commit/d33d096438c86ad342aed6aa2c9b1f706b52d050))
- resolve NotionClient initialization and add requests-mock for testing ([a2c1fd0](https://github.com/atxtechbro/notion-automation/commit/a2c1fd04b40e9c8dac534d2a1cf463118bbe038e))

### Features

- add CLI for database creation, update .gitignore, and remove old JSON configs ([e892ca2](https://github.com/atxtechbro/notion-automation/commit/e892ca235b8eb7d8f6c60af71a5f74c77a771ad1))
- Add Notion automation for workout plan creation and testing ([fefb05c](https://github.com/atxtechbro/notion-automation/commit/fefb05cd10ff98f2c65dcf44796c35e15f49dc9d))
- add semantic versioning automation with GitHub Actions ([376e249](https://github.com/atxtechbro/notion-automation/commit/376e249ba66056946412400e8d1e4d69b46caa2e))
- add support for specifying target Notion page ID via CLI ([80ae1b5](https://github.com/atxtechbro/notion-automation/commit/80ae1b5570771ed4eeac660f45c928668223a7ac))
- **cli:** support creating empty databases with schema-only option ([9b8d405](https://github.com/atxtechbro/notion-automation/commit/9b8d4054bc38e0fbaf72d9707fc5bd612ade2e36))
- **cli:** update README and improve create_database command ([d451459](https://github.com/atxtechbro/notion-automation/commit/d4514595bb0e6dbec200fc590fbdde880c07bb67))
- Combine schema and tasks into single JSON files for better organization ([1c96668](https://github.com/atxtechbro/notion-automation/commit/1c966682742344e052ba0946a3588ac29629c2f5))
- Integrate Notion API for database creation and task management ([386c38d](https://github.com/atxtechbro/notion-automation/commit/386c38d1e2df7dd6c6ec8c484247561931cf476b))
- Integrate Notion API for database creation and task management ([e53452a](https://github.com/atxtechbro/notion-automation/commit/e53452a1610c221dd6a5d5a206b9ddda5f642254))
- **models:** add support for 'checkbox' and 'multi_select' property types in schema and task validation ([7c1f1ca](https://github.com/atxtechbro/notion-automation/commit/7c1f1ca93ecac3f52a86be8ea6d760613d680c5b))
