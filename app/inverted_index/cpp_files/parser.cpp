#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <map>
#include <utility>
#include <cstdint>
#include <algorithm>

namespace py = pybind11;

using PostingList = std::pair<uint16_t, py::buffer>;
using PostingScoreMap = std::map<std::pair<uint16_t, uint16_t>, double>;
using PostingScorePair = std::pair<const std::pair<uint16_t, uint16_t>, double>;
using NonConstPostingScorePair = std::pair<std::pair<uint16_t, uint16_t>, double>;


struct MinHeapComparator {
    bool operator() (const PostingScorePair& pair1, const PostingScorePair& pair2) const {
        return pair1.second > pair2.second;
    }
};


PostingScoreMap scorePostingLists(const std::vector<PostingList>& postingLists, double inverseDocumentFrequency)
{
    // Gets a vector of posting lists and gives a score to each one based on their term frequency and inverse document frequency
    PostingScoreMap scores;

    for (const PostingList& postingList : postingLists) {
        // postingList.second is an array.array in Python, but in C++ is passed as a buffer object
        // request the buffer info
        py::buffer_info bufferInfo = postingList.second.request();

        // get the array's ptr and typecast it into a uint16_t pointer
        uint16_t* arrPtr = static_cast<uint16_t*>(bufferInfo.ptr);
        size_t amountToTraverse = bufferInfo.size;

        std::pair<uint16_t, uint16_t> posting(postingList.first, 0);

        // For each posting in the array, add it to the map of posting:scores
        for (size_t i = 0; i < amountToTraverse; i += 2) {
            posting.second = arrPtr[i];
            scores[posting] = arrPtr[i+1] * inverseDocumentFrequency;
        }
    }

    return scores;
}


std::vector<std::pair<uint16_t, uint16_t>> getTopScoringResults(const std::vector<PostingScoreMap>& mapOfScores)
{
    // 1st step: Merge each map (dict) of post ID to scores, into one map 
    PostingScoreMap mergedMap;

    for (const PostingScoreMap& mapOfScore : mapOfScores) {
        for (const PostingScorePair& postingAndScore : mapOfScore) {
            mergedMap[postingAndScore.first] += postingAndScore.second;
        }
    }

    // 2nd step: Use a vector as a container for a min heap. Push all pairs 
    //  in the merged map into this heap. Ensure size is <= 300
    std::vector<NonConstPostingScorePair> topResultsHeap;
    MinHeapComparator comparator;

    for (const auto& [postID, score] : mergedMap) {
        if (topResultsHeap.size() < 300) {
            topResultsHeap.push_back(NonConstPostingScorePair(postID, score));
            std::push_heap(topResultsHeap.begin(), topResultsHeap.end(), comparator);

        } else if (score > topResultsHeap[0].second) {
            std::pop_heap(topResultsHeap.begin(), topResultsHeap.end(), comparator);
            topResultsHeap.back() = NonConstPostingScorePair(postID, score);
            std::push_heap(topResultsHeap.begin(), topResultsHeap.end(), comparator);
        }
    }

    // 3rd step: Take away all the TF-IDF values from the topResultsHeap. In the process, 
    //  take the reversed version of the min heap so that max values are at the top.
    std::vector<std::pair<uint16_t, uint16_t>> topResults;

    for (int i = topResultsHeap.size()-1; i >= 0; i--)
        topResults.push_back(topResultsHeap[i].first);

    return topResults;
}


// pybind11 macro for building into a module
PYBIND11_MODULE(parser, m) {
    m.def("score_postinglists", &scorePostingLists);
    m.def("get_topscoring_results", &getTopScoringResults);
}