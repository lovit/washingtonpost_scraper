# Washington Post search scraper

워싱턴 포스트에서 질의어 검색을 하여 수집된 결과를 저장합니다.

| Argument | Type | Default | Note |
| --- | --- | --- | --- |
| directory | str | ./output | Output directory |
| sleep | float | 10 | Sleep time for each submission (post) |
| max_num | int | 10 | Number of scrapped articles |
| query | str | korea | Number of scrapped articles |

```
python searching_a_query.py --sleep 1 --max_num 3 --query korea
```

위 스크립트 코드로 수집된 결과는 `output/korea/` 폴더에 저장됩니다.