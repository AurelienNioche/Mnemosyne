#
# adapted from: parse_logs.py <Peter.Bienstman@UGent.be>
#
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MnemosyneDjango.settings")
django.setup()

import os
import sys

from openSM2sync.log_entry import EventTypes
from mnemosyne.libmnemosyne.file_formats.science_log_parser \
     import ScienceLogParser

from data_interface.models import Log, ParsedLogs   # , Cards


class LogDatabase(object):

    MAX_BEFORE_COMMIT = 100

    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.parser = ScienceLogParser(database=self)

        self.parsed_logs = []
        self.log = []

    def parse_directory(self):
        self._delete_indexes()  # Takes too long while parsing.
        filenames = [os.path.join(self.log_dir, filename) for filename in \
            sorted(os.listdir(str(self.log_dir))) if \
            filename.endswith(".bz2")]
        filenames_count = len(filenames)
        i = 0
        for counter, filename in enumerate(filenames):
            sys.stdout.flush()
            log_name = os.path.basename(filename)
            entry = ParsedLogs.objects.filter(log_name=log_name).first()
            if entry is not None:
                print("(%d/%d) %1.1f%% %s already parsed" % \
                      (counter + 1, filenames_count,
                      (counter + 1.) / filenames_count * 100,
                      os.path.basename(filename)))
                continue
            print("(%d/%d) %1.1f%% %s" % (counter + 1, filenames_count,
                (counter + 1.) / filenames_count * 100,
                os.path.basename(filename)))
            try:
                self.parser.parse(filename)
                i += 1
            except KeyboardInterrupt:
                print("Interrupted!")
                self.commit()
                exit()
            except:
                print("Can't open file, ignoring.")
            self.parsed_logs.append(ParsedLogs(log_name=log_name))
            if i >= self.MAX_BEFORE_COMMIT:
                print("Committing...", flush=True, end=' ')
                self.commit()
                print("Done!")
                i = 0
        self.commit()
        self._create_indexes()

    def commit(self):

        ParsedLogs.objects.bulk_create(self.parsed_logs)
        Log.objects.bulk_create(self.log)
        self.parsed_logs = []
        self.log = []

    def _delete_indexes(self):
        pass
        # self.con.execute("drop index if exists i_log_timestamp;")
        # self.con.execute("drop index if exists i_log_user_id;")
        # self.con.execute("drop index if exists i_log_object_id;")

    def _create_indexes(self):
        pass
        # self.con.execute("create index i_log_timestamp on log (timestamp);")
        # self.con.execute("create index i_log_user_id on log (user_id);")
        # self.con.execute("create index i_log_object_id on log (object_id);")

    def log_started_program(self, timestamp, program_name_version):
        # self.con.execute(
        #     """insert into log(user_id, event, timestamp, object_id)
        #     values(?,?,?,?)""",
        #     (self.parser.user_id, EventTypes.STARTED_PROGRAM, int(timestamp),
        #      program_name_version))
        pass

    def log_stopped_program(self, timestamp):
        # self.log.append(
        #     Log(user_id=self.parser.user_id,
        #         event=EventTypes.STOPPED_PROGRAM,
        #         timestamp=int(timestamp))
        # )
        # self.con.execute(
        #     "insert into log(user_id, event, timestamp) values(?,?,?)",
        #     (self.parser.user_id, EventTypes.STOPPED_PROGRAM, int(timestamp)))
        pass

    def log_started_scheduler(self, timestamp, scheduler_name):
        # self.log.append(
        #     Log(user_id=self.parser.user_id,
        #         event=EventTypes.STARTED_SCHEDULER,
        #         timestamp=int(timestamp),
        #         object_id=scheduler_name)
        # )
        # self.con.execute(
        #     """insert into log(user_id, event, timestamp, object_id)
        #     values(?,?,?,?)""",
        #     (self.parser.user_id, EventTypes.STARTED_SCHEDULER, int(timestamp),
        #     scheduler_name))
        pass

    def log_loaded_database(self, timestamp, machine_id, scheduled_count,
                            non_memorised_count, active_count):
        pass
        # self.log.append(
        #     Log(user_id=self.parser.user_id,
        #         event=EventTypes.LOADED_DATABASE,
        #         timestamp=int(timestamp),
        #         object_id=machine_id,
        #         acq_reps=scheduled_count,
        #         ret_reps=non_memorised_count,
        #         lapses=active_count
        #         )
        # )
        # self.con.execute(
        #     """insert into log(user_id, event, timestamp, object_id, acq_reps,
        #     ret_reps, lapses) values(?,?,?,?,?,?,?)""",
        #     (self.parser.user_id, EventTypes.LOADED_DATABASE, int(timestamp),
        #     machine_id, scheduled_count, non_memorised_count, active_count))

    def log_saved_database(self, timestamp, machine_id, scheduled_count,
                           non_memorised_count, active_count):
        # self.con.execute(
        #     """insert into log(user_id, event, timestamp, object_id, acq_reps,
        #     ret_reps, lapses) values(?,?,?,?,?,?,?)""",
        #     (self.parser.user_id, EventTypes.SAVED_DATABASE, int(timestamp),
        #     machine_id, scheduled_count, non_memorised_count, active_count))
        pass

    def log_added_card(self, timestamp, card_id):
        pass
        # self.con.execute(
        #     """insert into log(user_id, event, timestamp, object_id)
        #     values(?,?,?,?)""",
        #     (self.parser.user_id, EventTypes.ADDED_CARD, int(timestamp), card_id))

    def log_deleted_card(self, timestamp, card_id):
        pass
        # self.con.execute(
        #     """insert into log(user_id, event, timestamp, object_id)
        #     values(?,?,?,?)""",
        #     (self.parser.user_id, EventTypes.DELETED_CARD, int(timestamp), card_id))

    def log_repetition(self, timestamp, card_id, grade, easiness, acq_reps,
        ret_reps, lapses, acq_reps_since_lapse, ret_reps_since_lapse,
        scheduled_interval, actual_interval, thinking_time,
        next_rep, scheduler_data):
        pass
        # self.con.execute(\
        #     """insert into log(user_id, event, timestamp, object_id, grade,
        #     easiness, acq_reps, ret_reps, lapses, acq_reps_since_lapse,
        #     ret_reps_since_lapse, scheduled_interval, actual_interval,
        #     thinking_time, next_rep)
        #     values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        #     (self.parser.user_id, EventTypes.REPETITION, int(timestamp), card_id,
        #     grade, easiness, acq_reps, ret_reps, lapses, acq_reps_since_lapse,
        #     ret_reps_since_lapse, scheduled_interval, actual_interval,
        #     int(thinking_time), next_rep))

        self.log.append(
            Log(user_id=self.parser.user_id,
                event=EventTypes.REPETITION,
                timestamp=int(timestamp),
                object_id=card_id,
                grade=grade,
                easiness=easiness,
                acq_reps=acq_reps,
                ret_reps=ret_reps,
                lapses=lapses,
                acq_reps_since_lapse=acq_reps_since_lapse,
                ret_reps_since_lapse=ret_reps_since_lapse,
                scheduled_interval=scheduled_interval,
                actual_interval=actual_interval,
                thinking_time=int(thinking_time),
                next_rep=next_rep
                )
        )

    def set_offset_last_rep(self, card_id, offset, last_rep):
        pass
        # self.con.execute(
        #     """insert or replace into _cards(id, offset, last_rep)
        #     values(?,?,?)""",
        #     (card_id + self.parser.user_id, offset, int(last_rep)))

    def offset_last_rep(self, card_id):
        pass
        # sql_result = self.con.execute("""select offset, last_rep
        #    from _cards where _cards.id=?""",
        #    (card_id + self.parser.user_id, )).fetchone()
        # return sql_result["offset"], sql_result["last_rep"]

    def update_card_after_log_import(self, id, creation_time, offset):
        pass


if __name__ == "__main__":
    log = LogDatabase(log_dir="mnemosyne-data")
    log.parse_directory()
