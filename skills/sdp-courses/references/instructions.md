# SDP Courses MCP

This server authors course catalogs and curricula. It does not manage purchases, payments, learners, enrolments, progress, or certificates. Quiz score reporting is read-only: use `list_course_test_attempts` (filter by `course_id`, `type` lesson/final, `passed`) and `get_course_test_attempt` for per-question results with rationales.

Call `list_companies` first. Every other data tool requires explicit `company_id`.

## Create a course

Stage and complete a cover, then create the pending course:

```json
{"tool":"create_course_cover_upload","arguments":{"company_id":42,"staging_key":"intro-ai","name":"cover.jpg","mime_type":"image/jpeg","is_default":true}}
{"tool":"complete_course_cover_upload","arguments":{"company_id":42,"upload_id":"returned-uuid"}}
{"tool":"create_course","arguments":{"company_id":42,"title":"Introduction to AI","course_type_id":7,"amount":2500,"image_upload_ids":["returned-uuid"]}}
```

Use `import_course_cover_url` for a public image. Never send base64 through MCP.

## Simple and advanced authoring

Use `create_course_video_upload`, POST the raw file once as multipart field `file`, then poll `complete_course_video_upload`. This direct flow supports files under 200 MB.

For advanced courses, create chapters and lessons, then use `set_course_lesson_html`, a video upload with `lesson_id`, `create_course_lesson_pdf_upload`, or `replace_course_lesson_quiz`. Reordering requires every chapter and lesson exactly once.

`replace_course_lesson_quiz` and `replace_course_final_test` are atomic. Each question requires at least two choices and one ID in `correct_choice_ids`.

Use `replace_course_collection_rules` for dynamic collections or `set_course_collection_membership` for explicit IDs. Deactivate collections with `update_course_collection`. Archive and restore courses instead of deleting them.

## Catalog images (course type covers, course collection covers)

`import_catalog_image_url` and `create_catalog_image_upload` + `complete_catalog_image_upload` produce an unattached `file_id`; nothing is visible on any record until `attach_catalog_image` is called. This covers course types and course collections — one set of tools, no per-entity image tools. Courses themselves keep their own dedicated cover tools (`import_course_cover_url` / `create_course_cover_upload` / `complete_course_cover_upload`) shown above.

```json
{"tool":"import_catalog_image_url","arguments":{"company_id":42,"url":"https://cdn.example.com/ai-icon.png"}}
{"tool":"attach_catalog_image","arguments":{"company_id":42,"target_type":"course_type","target_id":7,"file_id":"returned-file-id"}}
```

`target_type` accepts `course_type` or `course_collection`.

Common errors are `stale_membership_version`, `permission_denied`, `COURSES_NOT_AVAILABLE`, `validation_error`, and `not_found`.
