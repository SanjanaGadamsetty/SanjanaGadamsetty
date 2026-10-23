# Neon Tech — 40 switches

Every switch in `config/features.json` controls whether a corresponding `<details>` section appears in the generated README. **Visibility is fully implemented for all 40.** Turning a switch on does **not** automatically install a third-party service or start a new GitHub Action. The pre-existing `snake.yml` and `refresh-dashboard.yml` continue independently, even when their display switches are off.

## Working display modules

- Existing generated SVGs: `contribution_snake`, `contribution_activity_graph`, `github_stats_cards`, `most_used_languages`, `pull_request_tracker`, `latest_github_activity`, `featured_repository_rotation`.
- Rendered visuals and static content: `animated_typing_header`, `dynamic_neofetch_card`, `terminal_status_dashboard`, `milestone_tracker`, `dsa_progress_tracker`, `daily_developer_quote`, `currently_building`, `learning_progress_dashboard`.
- Links to real profiles/activity: `contribution_heatmap`, `year_in_code_calendar`, `repository_statistics`, `leetcode_statistics`, `codeforces_rating_tracker`, `codechef_rating_tracker`, `hackerrank_badges`, `daily_coding_challenge`, `issue_contribution_tracker`, `open_source_journey_timeline`.

**Important:** The link-based modules are *not* embedded live statistic cards. The `featured_repository_rotation` module currently displays the existing recent-projects SVG; it does not animate a rotation. `animated_typing_header` uses an external SVG provider. Some cards are repeated elsewhere in the original README because the existing content is preserved.

## Setup-required modules

`pacman_graph`, `contribution_skyline_3d`, `contribution_galaxy`, `github_streak_stats`, `github_trophy_wall`, `github_metrics_dashboard`, `productive_hours_graph`, `contributor_leaderboard`, `developer_radar_chart`, `developer_xp_system`, `github_achievement_game`, `cosmic_developer_dashboard`, `wakatime_statistics`, `latest_blog_posts`, `spotify_now_playing`.

If enabled before their integrations are built, these show a **clearly labeled setup-required message**, not fake stats or a broken image. Some links can be configured in `config/profile.json`, but a profile link is not a live API integration.

## Existing README sections

The original terminal, profile description, stats, projects, and snake are left intact **outside** the managed feature section. The switches control only the 40 modules inside `<!-- SANJANAOS:FEATURES:START -->` and `<!-- SANJANAOS:FEATURES:END -->`. If you want an existing standalone section hidden too, move it into the managed generator first; do not delete your existing workflow files.
