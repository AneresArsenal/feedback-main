import { connect } from 'react-redux'
import { compose } from 'redux'
import withQueryRouter from 'with-query-router'
import { selectCurrentUser } from 'with-react-redux-login'

import FormFooter from './FormFooter'
import selectRoleByUserIdAndType from '../../../../selectors/selectRoleByUserIdAndType'
import selectCurrentUserReviewByArticleId from '../../../../selectors/selectCurrentUserReviewByArticleId'


const mapStateToProps = (state, ownProps) =>  {
  const {
    match: { params: { articleId } },
  } = ownProps
  const currentUser = selectCurrentUser(state)
  const { id: currentUserId } = currentUser || {}

  const editorRole = selectRoleByUserIdAndType(state, currentUserId, 'editor')
  const reviewerRole = selectRoleByUserIdAndType(state, currentUserId, 'reviewer')

  const canReview = typeof reviewerRole !== 'undefined'
  const canEdit = typeof editorRole !== 'undefined'

  return {
    canEdit,
    canReview,
    review: selectCurrentUserReviewByArticleId(state, articleId)
  }
}

export default compose(
  withQueryRouter(),
  connect(mapStateToProps)
)(FormFooter)
