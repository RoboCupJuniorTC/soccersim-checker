from . import app, appbuilder
from app.models import Upload
import logging
import sys
import atexit
import datetime
import subprocess


my_subprocess = []


@atexit.register
def finish_my_subprocess():
    for process in my_subprocess:
        logging.warn('Killing subprocess: %d', process.pid)
        process.terminate()


@app.cli.command('process-next-match')
def process_next_match():
    logging.info('Processing next match')

    session = appbuilder.get_session()
    uploaded_query = session \
        .query(Upload) \
        .filter(Upload.status == 'Uploaded')

    in_progress_query = session \
        .query(Upload) \
        .filter(Upload.status == 'InProgress')

    n_uploaded = uploaded_query.count()
    n_in_progress = in_progress_query.count()

    logging.info('Status report: in_progress/uploaded %d/%d', n_in_progress,
                 n_uploaded)

    if n_in_progress != 0:
        logging.warn('Non-zero number of InProgress uploads (%d), bailing.',
                     n_in_progress)
        sys.exit(1)

    first_uploaded = uploaded_query.first()

    if first_uploaded is None:
        logging.warn('No uploads to process, bailing.')
        sys.exit(0)

    team_id = first_uploaded.changed_by.last_name

    first_uploaded.status = 'InProgress'

    session.add(first_uploaded)
    session.commit()

    timestamp = datetime.datetime.now().strftime('%Z%Y%m%d_%H%M%S')
    with open(f"logs/{timestamp}_{team_id}.log", 'w') as fp:
        cmd_str = f"bash run.sh {team_id} 999 {timestamp}_test_{team_id}"
        logging.info("\tExecuting: `%s`, log: %s", cmd_str, fp.name)
        proc = subprocess.Popen(cmd_str.split(' '),
                                stdout=fp,
                                stderr=fp,
                                text=True)
        my_subprocess.append(proc)
        proc.communicate()
        my_subprocess.remove(proc)

    first_uploaded.status = 'Simulated'

    session.add(first_uploaded)
    session.commit()
