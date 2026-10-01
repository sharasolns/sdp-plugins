---
name: sdp-courses
description: Administer SDP courses through Courses MCP on the themes host. Use for course types, collections, covers, videos, chapters, lessons, PDFs, quizzes, final tests, and course lifecycle changes. Do not use for purchases, learners, enrolments, progress, certificates, or storefront HTML. Read-only quiz attempt results are supported.
---

# SDP Courses

The user must already have an SDP account at https://sdp-platform.com. If OAuth fails, send them there to sign up or sign in first. Do not invent API keys.

Call `list_companies` first. Every tool except `list_companies` and `open_courses_dashboard` requires explicit numeric `company_id`.

Read `sdp://courses/instructions` before creating or mutating course records. Do not invent course, type, collection, chapter, lesson, image, or video ids.

## Authoring

Create at least one completed staged cover before `create_course`; new courses are always pending. Use explicit lifecycle tools to activate, archive, or restore. Simple courses need a course-level video before activation. Advanced courses need at least one configured lesson item.

Use direct upload creation and completion tools for covers, videos under 200 MB, and lesson PDFs up to 50 MB. Never send base64 through MCP. Use the dashboard for larger TUS video uploads.

Curriculum mutations are granular. Quiz and final-test replacement is atomic. Changing a lesson item type preserves inactive material until an explicit delete or replacement operation removes it.

## Storefront

Website Builder only renders `{sdpGetCourses}` / `{sdpGetCourse}` pages. Link items to `/courses/{$course->slug}`. The chapter/lesson tree is a lightweight public outline; do not infer or expose lesson HTML, PDFs, quizzes, playback URLs, enrolment state, or learner progress. Course purchases, enrolments, learner progress, and certificates are outside Courses MCP. Read quiz results with `list_course_test_attempts` and `get_course_test_attempt`; these tools do not change learner progress.

## Instruction reference

Read [references/instructions.md](references/instructions.md) for source-exported workflows and examples. Refresh the hosted instruction resource before mutations; it takes precedence over this bundled snapshot.

For course type or collection images, use `import_catalog_image_url` or the catalog direct-upload flow, then `attach_catalog_image` with the returned `file_id`. Upload completion alone does not attach the image.
