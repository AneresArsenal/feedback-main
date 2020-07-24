import React, { useCallback, useMemo, useState } from 'react'
import { useDispatch } from 'react-redux'
import { useLocation, useHistory } from 'react-router-dom'
import { requestData } from 'redux-thunk-data'

import Main from 'components/layout/Main'
import Header from 'components/layout/Header'
import Footer from 'components/layout/Footer'
import Controls from 'components/layout/Feeds/Controls'
import Icon from 'components/layout/Icon'
import Items from 'components/layout/Feeds/Items'
import VerdictItem from 'components/layout/VerdictItem'
import KeywordsBar from 'components/layout/Feeds/Controls/KeywordsBar'

import { verdictNormalizer } from 'utils/normalizers'


export default () => {
  const history = useHistory()
  const { search } = useLocation()
  const dispatch = useDispatch()
  const [showMoreStatus, setShowMoreStatus] = useState(false)

  const config = useMemo(
    () => ({
      apiPath: `/verdicts${search}`,
      normalizer: verdictNormalizer,
    }),
    [search]
  )


  const renderItem = useCallback(item => <VerdictItem verdict={item} />, [])

  const handleKeywordsChange = useCallback(
    (key, value) => history.push(`/verdicts?keywords=${value}`),
    [history]
  )

  const showMore = useCallback(() => {
      setShowMoreStatus(true)
      dispatch(requestData({
        apiPath: '/verdicts',
        normalizer: verdictNormalizer
      }), [dispatch])
      history.push('/verdicts')
    },
    [history]
  )


  return (
    <>
      <Header withLinks />
      <Main className="landing with-header">
        <section className="hero">
          <div className="container">
            <p className="h1">
              <b>
                {'2000'}
              </b>
              {' articles fact-checked'}
              <br />
              {'by '}
              <b>
                {'14450'}
              </b>
              {' Scientists'}
            </p>
            <KeywordsBar
              layout='vertical'
              onChange={handleKeywordsChange}
            />
          </div>
        </section>

        <section className="verdicts">
          <div className="container">
            <div className="section-title">
              <span className="icon-container">
                <Icon
                  className="icon"
                  name="ico-review.svg"
                />
              </span>
              <h3>
                {'Recent Claims'}
              </h3>
              <div className="verdict-items">
                <Items
                  config={config}
                  loadMore={showMoreStatus}
                  renderItem={renderItem}
                />
                <div className="show-more">
                  <button
                    onClick={showMore}
                    type='button'
                  >
                    {'Show more'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </Main>
      <Footer />
    </>
  )
}
