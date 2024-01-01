import json
import re
def torrentio(body):
  data = json.loads(body)
  new_body = {"streams": []}

  for element in data['streams']:
      element['torrent'] = 'magnet:?xt=urn:btih:' + element['infoHash']
      element['quality'] = element['behaviorHints']['bingeGroup']

      seeds = element['title'].split('👤')
      element['seeds'] = re.search(r'\d+', seeds[1]).group() if seeds[1] else 1

      size = re.search(r'💾(.*)⚙️', element['title'])
      element['size'] = size.group(1).strip() if size else 1

      element['title'] = element['title'].replace("👤", "[seeds]").replace("💾", "").replace("⚙️", "").replace('\n', '-')

      new_body['streams'].append(element)

  body = json.dumps(new_body)

  return body