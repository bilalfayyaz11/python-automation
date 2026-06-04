# Artifact Version Management and Release Automation

## What This Does

This system automates semantic versioning, artifact packaging, build metadata generation, checksum verification, Git tagging, and release tracking for software delivery pipelines. It creates versioned application artifacts and attaches traceable metadata including build number, build date, source commit, branch, checksum, artifact size, and build environment.

The implementation demonstrates how release engineering teams maintain artifact provenance and verify integrity across CI/CD workflows. This is important in production environments where teams must know exactly which source code created a build, when it was built, and whether the artifact changed after creation.

## Architecture

+---------------------------+
| Source Application        |
| src/app.sh                |
+------------+--------------+
             |
             v
+---------------------------+
| Version Manager           |
| VERSION + CHANGELOG       |
+------------+--------------+
             |
             v
+---------------------------+
| Release Automation        |
| release.sh                |
+------------+--------------+
             |
             v
+---------------------------+
| Build System              |
| build.sh                  |
+------------+--------------+
             |
      +------+------+
      |             |
      v             v
+-----------+   +----------------+
| Artifact  |   | Build Metadata |
| .tar.gz   |   | JSON + SHA256  |
+-----------+   +----------------+
      |             |
      +------+------+
             |
             v
+---------------------------+
| Git Release Tag           |
| vMAJOR.MINOR.PATCH        |
+---------------------------+

## Prerequisites

- Ubuntu Linux
- Git
- jq
- build-essential
- tar
- sha256sum
- Bash shell

## Setup & Installation

sudo apt update

sudo apt install -y git jq build-essential tree

## How to Reproduce

1. Clone this repository.
2. Enter the implementation directory.

   cd artifact-version-management

3. Initialize or inspect the current version.

   ./version-manager.sh get

4. Run a patch release.

   ./release.sh patch "Bug fixes and improvements"

5. List generated artifacts.

   ./query-artifacts.sh list

6. Inspect artifact metadata.

   ./query-artifacts.sh info $(cat VERSION)

7. Verify artifact integrity.

   artifact=$(ls builds/*.tar.gz | head -1)
   ./query-artifacts.sh verify "$artifact"

8. Run the complete verification script.

   ./verify-release-system.sh

## Tools Used

- Bash
- Git
- Git Tags
- jq
- tar
- sha256sum
- Linux
- Semantic Versioning
- JSON Metadata

## Key Skills Demonstrated

- Semantic versioning automation
- Release workflow automation
- Artifact packaging
- Build metadata generation
- Git tag creation and release tracking
- Checksum-based artifact integrity verification
- Artifact provenance tracking
- Bash scripting for CI/CD workflows
- Software delivery pipeline foundations

## Real-World Use Case

This pattern is used in CI/CD pipelines where every release must produce a traceable artifact. DevOps and platform teams use metadata, checksums, and Git tags to connect deployable files back to source commits, release versions, build numbers, and build environments. This enables safe rollbacks, compliance audits, production incident investigation, and supply chain integrity validation.

## Lessons Learned

- Semantic versioning makes release impact easier to understand.
- Build metadata creates traceability between source code and deployable artifacts.
- Checksums help verify that artifacts were not modified after creation.
- Git tags provide stable release markers in version control.
- Automated release scripts reduce human error during repetitive delivery workflows.

## Troubleshooting Log

- Implemented missing version parsing and validation logic.
- Added changelog generation instead of only printing a success message.
- Generated build metadata with artifact size, checksum, source commit, branch, builder, and OS details.
- Fixed artifact verification to read metadata from the correct metadata directory.
- Added complete verification automation for version files, artifacts, metadata, Git tags, and checksum integrity.
