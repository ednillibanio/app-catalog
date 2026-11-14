English | [Português](ci-devsecops.pt-BR.md)

# CI and DevSecOps outcomes

Each app documents its validation commands and ownership. CI should cover repository hygiene, secret detection, pull request metadata, relevant build and tests, static analysis, dependencies and software bills of materials when applicable. Identify required versus informational checks and make scanner execution failures visible separately from findings. Record accepted findings, owners and follow-up issues; do not claim coverage without evidence.

The public personal `ci-workflows` repository publishes reusable pre-commit hooks and GitHub Actions workflows. Pin hooks to a released SemVer tag and reusable workflows to full commit SHAs. This catalog consumes hooks locally; it does not yet run automated CI. Apps keep their existing CI until an adoption plan authorizes and validates the relevant interfaces. Give CI only necessary permissions and do not expose secrets to untrusted pull requests. This standard does not implement jobs, publish images, deploy, or specify installation of developer environments.
