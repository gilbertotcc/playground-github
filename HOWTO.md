# GitHub metrics

Steps:

TODO: Get all the PRs closed or merged within a period

```shell
gh search prs --owner=totmoney --state=closed "closed:2025-07-01..2025-07-07" \
  --json=id,number,author,title,commentsCount,repository,url,createdAt,updatedAt,closedAt \
  --limit=1000 --sort=updated --order=desc
```
