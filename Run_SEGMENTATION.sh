#!/bin/bash
python ./MEMSeg/add_space.py Test_SAMPLE.utf8 ./MEMSeg/text_split.utf8
python ./MEMSeg/postagger/maxent_tagger.py -m ./MEMSeg/pku_tagger.model ./MEMSeg/text_split.utf8 > ./MEMSeg/text_tag.utf8
python ./MEMSeg/split_by_four_tag.py ./MEMSeg/text_tag.utf8 MEMSeg_RESULT.utf8
python ./SelfSeg/SelfSeg.py Test_SAMPLE.utf8 SelfSeg_RESULT.utf8
