from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm
import argparse
import re
import os
import json
import shutil
import locale

locale.setlocale(locale.LC_TIME, 'ko_KR.UTF-8')

env = Environment(loader=FileSystemLoader('templates'))


def draw_youtube(link):
    tmpl = env.get_template('youtube.html.j2')

    found = re.match(r'https://www\.youtube\.com/watch\?v=(.+)', link)
    if found:
        return tmpl.render(id=found.group(1))
    return ''


def draw_image(attachment):
    tmpl = env.get_template('image.html.j2')

    if attachment != '':
        return tmpl.render(filename=attachment)
    return ''


def draw_response(board_id, thread_id, response):
    tmpl = env.get_template('response.html.j2')

    date=datetime.strptime(response['createdAt'], '%Y-%m-%dT%H:%M:%S.000Z')

    return tmpl.render(
        response_id=f'response_{board_id}_{thread_id}_{response['sequence']}',
        sequence=response['sequence'],
        username=response['username'],
        user_id=response['userId'],
        created_at=date.strftime("%Y-%m-%d (%a) %H:%M:%S"),
        youtube=draw_youtube(response['youtube']),
        image=draw_image(response['attachment']),
        content=response['content']
    )


def draw_responses(board_id, thread_id, responses):
    section = []

    for response in responses:
        section.append(draw_response(board_id, thread_id, response))

    return '\n'.join(section)


def draw_thread(thread):
    tmpl = env.get_template('thread.html.j2')

    create_date = datetime.strptime(thread['createdAt'], '%Y-%m-%dT%H:%M:%S.000Z')
    update_date = datetime.strptime(thread['updatedAt'], '%Y-%m-%dT%H:%M:%S.000Z')

    return tmpl.render(
        board_id=thread['boardId'],
        id=thread['threadId'],
        title=thread['title'],
        size=thread['size'],
        username=thread['username'],
        created_at=create_date.strftime("%Y-%m-%d (%a) %H:%M:%S"),
        updated_at=update_date.strftime("%Y-%m-%d (%a) %H:%M:%S"),
        responses=draw_responses(
            thread['boardId'],
            thread['threadId'],
            thread['responses']
        )
    )


def draw_trace(thread):
    tmpl = env.get_template('trace.html.j2')

    return tmpl.render(
        title=thread['title'],
        thread=draw_thread(thread),
        board_id=thread['boardId'],
        thread_id=thread['threadId'],
    )


def build_trace(board_data_dir, board_dist_dir):
    tf_pattern = r'^\d+\.json$'

    json_files = [f for f in os.listdir(board_data_dir) if re.match(tf_pattern, f)]
    json_files.sort()
    progress = tqdm(json_files)

    for json_file in progress:
        src_file = os.path.join(board_data_dir, json_file)

        with open(src_file, 'r', encoding='utf-8') as sf:
            thread = json.load(sf)
            progress.set_postfix(thread=str(thread['threadId']))
            page = draw_trace(thread)

            dst_dir = os.path.join(board_dist_dir, str(thread['threadId']))
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)

            dst_file = os.path.join(dst_dir, 'index.html')
            with open(dst_file, 'w', encoding='utf-8') as df:
                df.write(page)

            image_dir = os.path.join(board_dist_dir, str(thread['threadId']), 'image')
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            images = [response['attachment'] for response in thread['responses'] if response['attachment'] != '']
            for image in images:
                image_src = os.path.join(board_data_dir, 'data', image)
                image_dst = os.path.join(image_dir, image)
                shutil.copy(image_src, image_dst)


def filter_index(index):
    filtered_data = []
    for item in index:
        filtered_item = {key: item[key] for key in ['threadId', 'title', 'username'] if key in item}
        filtered_data.append(filtered_item)
    return json.dumps(filtered_data, ensure_ascii=False)


def build_index(board_data_dir, board_dist_dir, board_id):
    src_file = os.path.join(board_data_dir, 'index.json')

    with open(src_file, 'r', encoding='utf-8') as sf:
        index = sorted(json.load(sf), key=lambda x: x['threadId'])

        if not os.path.exists(board_dist_dir):
            os.makedirs(board_dist_dir)

        tmpl = env.get_template('index.html.j2')
        page = tmpl.render(
            title=board_id,
            threads=filter_index(index),
        )

        dst_file = os.path.join(board_dist_dir, 'index.html')
        with open(dst_file, 'w', encoding='utf-8') as df:
            df.write(page)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('board_id', type=str)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--trace-only', action='store_true')
    group.add_argument('--index-only', action='store_true')
    args = parser.parse_args()

    board_data_dir = f'./data/{args.board_id}'
    board_dist_dir = f'./dist/{args.board_id}'

    if args.trace_only:
        build_trace(board_data_dir, board_dist_dir)
    elif args.index_only:
        build_index(board_data_dir, board_dist_dir, args.board_id)
    else:
        build_trace(board_data_dir, board_dist_dir)
        build_index(board_data_dir, board_dist_dir, args.board_id)


if __name__ == "__main__":
    main()
