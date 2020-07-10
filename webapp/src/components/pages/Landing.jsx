import React, { useCallback, useMemo } from 'react'
import { useLocation, useHistory } from 'react-router-dom'

import Main from 'components/layout/Main'
import Header from 'components/layout/Header'
import Footer from 'components/layout/Footer'
import Icon from 'components/layout/Icon'
import Items from 'components/layout/Feeds/Items'
import VerdictItem from 'components/layout/VerdictItem'
import KeywordsBar from 'components/layout/Feeds/Controls/KeywordsBar'

import { verdictNormalizer } from 'utils/normalizers'


export default () => {
  const history = useHistory()
  const { search } = useLocation()


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


  return (
    <>
      <Header withMenu />
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
              <div className="items">
                <Items
                  config={config}
                  renderItem={renderItem}
                />
              </div>
            </div>
          </div>
        </section>
      </Main>
      <Footer />
    </>
  )
}
