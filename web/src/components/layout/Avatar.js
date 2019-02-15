import PropTypes from 'prop-types'
import React from 'react'
import { connect } from 'react-redux'
import { selectCurrentUser } from 'with-login'

import { Icon } from './Icon'
import { THUMBS_URL } from '../../utils/config'

const Avatar = ({ className, user, whiteHeader }) => {
  if (user) {
    const backgroundStyle = {
      backgroundImage: `url('${THUMBS_URL}/users/${user.id}')`,
      backgroundSize: 'cover',
    }
    return <div className={className} style={backgroundStyle} />
  }
  return (
    <span className='icon'>
      <Icon svg={`ico-user-circled${whiteHeader ? '-w' : ''}`} />
    </span>
  )
}

Avatar.defaultProps = {
  className: 'avatar',
  user: null,
  whiteHeader: null,
}

Avatar.propTypes = {
  className: PropTypes.string,
  user: PropTypes.oneOfType([PropTypes.object, PropTypes.bool]),
  whiteHeader: PropTypes.bool,
}

function mapStateToProps(state, ownProps) {
  return {
    user: ownProps.user || selectCurrentUser(state),
  }
}

export default connect(mapStateToProps)(Avatar)